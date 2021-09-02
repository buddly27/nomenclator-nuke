# -*- coding: utf-8 -*-

import collections
import copy
import os

import nomenclator.utilities
import nomenclator.template


#: Context Structure type.
Context = collections.namedtuple(
    "Context", [
        "location_path",
        "recent_locations",
        "path",
        "suffix",
        "version",
        "description",
        "descriptions",
        "append_username_to_name",
        "padding",
        "paddings",
        "create_subfolders",
        "tokens",
        "username",
        "template_configs",
        "outputs"
    ]
)


#: Output Context Structure type.
OutputContext = collections.namedtuple(
    "OutputContext", [
        "name",
        "blacklisted_names",
        "path",
        "passname",
        "enabled",
        "destination",
        "destinations",
        "file_type",
        "file_types",
        "multi_views",
        "colorspace",
        "append_username_to_name",
        "append_colorspace_to_name",
        "append_passname_to_name",
        "append_passname_to_subfolder",
    ]
)


def fetch(config, is_project=False):
    """Fetch context object.

    :param config: :class:`~nomenclator.config.Config` instance.

    :param is_project: Indicate whether the project context is requested.
        Default is False, which means that the composition context will be
        returned.

    :return: :class:`Context` instance.

    """
    recent_locations = nomenclator.utilities.fetch_recent_comp_paths(
        max_values=config.max_locations
    )
    paddings = nomenclator.utilities.fetch_paddings(
        max_value=config.max_padding
    )

    if not is_project:
        template_configs = config.comp_template_configs
        outputs = fetch_outputs(config)
        suffix = "nk"

    else:
        template_configs = config.project_template_configs
        outputs = tuple()
        suffix = "hrox"

    return Context(
        location_path="",
        recent_locations=recent_locations,
        path="",
        suffix=suffix,
        version=None,
        description=_fetch_item(config.descriptions, 0),
        descriptions=config.descriptions,
        append_username_to_name=False,
        padding=_fetch_item(paddings, 0),
        paddings=paddings,
        create_subfolders=config.create_subfolders,
        tokens=config.tokens,
        username=config.username,
        template_configs=template_configs,
        outputs=outputs
    )


def fetch_outputs(config):
    """Fetch list of output context objects.

    An output context is returned for each matching output node.

    :param config: :class:`~nomenclator.config.Config` instance.

    :return: Tuple of :class:`OutputContext` instances.

    """
    nodes, node_names = nomenclator.utilities.fetch_nodes()

    outputs = []

    colorspace_mapping = dict(config.colorspace_aliases)

    for node in sorted(nodes, key=lambda n: n.name()):
        blacklisted = tuple([n for n in node_names if n != node.name()])

        file_types = [
            label.split()[0].strip() for label
            in node["file_type"].values()
            if len(label.split())
        ]

        # Resolve colorspace value if node have a colorspace knob.
        knob = node.knob("colorspace")
        colorspace = knob.value() if knob is not None else "none"
        colorspace = colorspace_mapping.get(colorspace, colorspace)

        context = OutputContext(
            name=node.name(),
            blacklisted_names=blacklisted,
            path=node["file"].value(),
            passname=node.name(),
            enabled=not node["disable"].value(),
            destination="",
            destinations=tuple(),
            file_type=node["file_type"].value().strip() or "exr",
            file_types=tuple(file_types),
            multi_views=len(node["views"].value().split()) > 1,
            colorspace=colorspace,
            append_username_to_name=False,
            append_colorspace_to_name=False,
            append_passname_to_name=False,
            append_passname_to_subfolder=False
        )
        outputs.append(context)

    return tuple(outputs)


def _fetch_item(items, index):
    """Return item *index* from incoming list or None."""
    return items[index] if len(items) else None


def update(context):
    """Return updated context object with generated paths.

    Incoming *context* will not be mutated.

    :param context: :class:`Context` instance.

    :return: updated :class:`Context` instance.

    """
    token_mapping = dict(context.tokens)

    config = nomenclator.utilities.fetch_template_config(
        context.location_path,
        context.template_configs,
        token_mapping
    )
    if config is None:
        # noinspection PyProtectedMember
        return context._replace(
            path="",
            version=None,
            outputs=update_outputs(context, [], {})
        )

    version = nomenclator.utilities.fetch_next_version(
        context.location_path, config.pattern_path, token_mapping
    )

    # Update token values.
    token_mapping.update({
        "version": "{0:03d}".format(version),
        "padding": context.padding,
        "description": context.description,
        "username": context.username
    })

    name = nomenclator.template.generate_scene_name(
        config.pattern_base, context.suffix,
        append_username=context.append_username_to_name,
        token_mapping=token_mapping
    )

    # noinspection PyProtectedMember
    return context._replace(
        path=os.path.join(context.location_path, name),
        version=version,
        outputs=update_outputs(context, config.outputs, token_mapping)
    )


def update_outputs(contexts, template_configs, token_mapping):
    """Return updated output context objects with generated paths.

    Incoming *contexts* will not be mutated.

    :param contexts: :Tuple of :class:`OutputContext` instances.

    :param template_configs: List of available
        :class:`~nomenclator.config.TemplateConfig` instances.

    :param token_mapping: Mapping regrouping resolved token values associated
        with their name.

    :return: Tuple of :class:`OutputContext` instances.

    """
    mapping = {config.id: config for config in template_configs}

    _contexts = []

    for _context in contexts:
        config = mapping.get(_context.destination)
        if config is None:
            # noinspection PyProtectedMember
            _contexts.append(_context._replace(path=""))
            continue

        # Update token values.
        _token_mapping = copy.deepcopy(token_mapping)
        _token_mapping.update({
            "colorspace": _context.colorspace,
            "passname": _context.passname,
        })

        path = nomenclator.template.resolve(config.pattern_path, _token_mapping)
        name = nomenclator.template.generate_output_name(
            config.pattern_base,
            _context.file_type,
            append_passname_to_subfolder=_context.append_passname_to_subfolder,
            append_passname=_context.append_passname_to_name,
            append_colorspace=_context.append_colorspace_to_name,
            append_username=_context.append_username_to_name,
            multi_views=_context.multi_views,
            token_mapping=_token_mapping
        )

        # noinspection PyProtectedMember
        _contexts.append(_context._replace(path=os.path.join(path, name)))

    return tuple(_contexts)
