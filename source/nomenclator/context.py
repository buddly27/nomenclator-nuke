# -*- coding: utf-8 -*-

import collections

import nomenclator.utilities


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

        colorspace = node["colorspace"].value()
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
