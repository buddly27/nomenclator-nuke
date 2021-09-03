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
        "outputs",
        "error",
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
        "error",
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
    paddings = nomenclator.utilities.fetch_paddings(
        max_value=config.max_padding
    )

    if not is_project:
        path = nomenclator.utilities.fetch_current_comp_path()
        template_configs = config.comp_template_configs
        suffix = "nk"
        recent_locations = nomenclator.utilities.fetch_recent_comp_paths(
            max_values=config.max_locations,
        )

        # Fetch matching output template configs if possible.
        if len(path):
            template_config = nomenclator.utilities.fetch_template_config(
                os.path.dirname(path), template_configs, {}
            )
            outputs = fetch_outputs(config, getattr(template_config, "outputs", []))
        else:
            outputs = fetch_outputs(config, [])

    else:
        path = nomenclator.utilities.fetch_current_project_path()
        template_configs = config.project_template_configs
        suffix = "hrox"
        recent_locations = nomenclator.utilities.fetch_recent_project_paths(
            max_values=config.max_locations,
        )

        outputs = tuple()

    return Context(
        location_path=os.path.dirname(path),
        recent_locations=recent_locations,
        path=path,
        suffix=suffix,
        version=None,
        description=config.default_description,
        descriptions=config.descriptions,
        append_username_to_name=False,
        padding=config.default_padding,
        paddings=paddings,
        create_subfolders=config.create_subfolders,
        tokens=config.tokens,
        username=config.username,
        template_configs=template_configs,
        outputs=outputs,
        error=None
    )


def fetch_outputs(config, template_configs):
    """Fetch list of output context objects.

    An output context is returned for each matching output node.

    :param config: :class:`~nomenclator.config.Config` instance.

    :param template_configs: List of
        :class:`~nomenclator.config.OutputTemplateConfig` instances.

    :return: Tuple of :class:`OutputContext` instances.

    """
    outputs = []

    nodes, node_names = nomenclator.utilities.fetch_nodes()
    alias_mapping = dict(config.colorspace_aliases)

    mapping = {config.id: config for config in template_configs}
    destinations = tuple(sorted(mapping.keys()))

    for node in sorted(nodes, key=lambda n: n.name()):
        path = nomenclator.utilities.fetch_output_path(node)
        blacklisted = tuple([n for n in node_names if n != node.name()])

        _config = None

        # Fetch matching config to initiate default values if possible
        if len(template_configs) and len(path):
            _config = nomenclator.utilities.fetch_output_template_config(
                os.path.dirname(path), template_configs
            )

        # Initiate first destination if possible
        if _config is None and len(destinations):
            _config = mapping.get(destinations[0])

        if _config is not None:
            destination = _config.id
            append_username_to_name = _config.append_username_to_name
            append_colorspace_to_name = _config.append_colorspace_to_name
            append_passname_to_name = _config.append_passname_to_name
            append_passname_to_subfolder = _config.append_passname_to_subfolder

        else:
            destination = ""
            append_username_to_name = False
            append_colorspace_to_name = False
            append_passname_to_name = False
            append_passname_to_subfolder = False

        context = OutputContext(
            name=node.name(),
            blacklisted_names=blacklisted,
            path=path,
            passname=node.name(),
            enabled=nomenclator.utilities.is_enabled(node),
            destination=destination,
            destinations=destinations,
            file_type=nomenclator.utilities.fetch_file_type(node, "exr"),
            file_types=nomenclator.utilities.fetch_file_types(node),
            multi_views=nomenclator.utilities.has_multiple_views(node),
            colorspace=nomenclator.utilities.fetch_colorspace(node, alias_mapping),
            append_username_to_name=append_username_to_name,
            append_colorspace_to_name=append_colorspace_to_name,
            append_passname_to_name=append_passname_to_name,
            append_passname_to_subfolder=append_passname_to_subfolder,
            error=None
        )
        outputs.append(context)

    return tuple(outputs)


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
            outputs=update_outputs(context.outputs, [], {}),
            error=_update_error(context)
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

    try:
        name = nomenclator.template.generate_scene_name(
            config.pattern_base, context.suffix,
            append_username=context.append_username_to_name,
            token_mapping=token_mapping
        )
    except Exception as exception:
        # noinspection PyProtectedMember
        return context._replace(
            path="",
            version=None,
            outputs=update_outputs(context.outputs, [], {}),
            error=_update_error(context, error=(config, exception))
        )

    else:
        # noinspection PyProtectedMember
        return context._replace(
            path=os.path.join(context.location_path, name),
            version=version,
            outputs=update_outputs(
                context.outputs, config.outputs, token_mapping
            ),
            error=None
        )


def update_outputs(contexts, template_configs, token_mapping):
    """Return updated output context objects with generated paths.

    Incoming *contexts* will not be mutated.

    :param contexts: :Tuple of :class:`OutputContext` instances.

    :param template_configs: List of available
        :class:`~nomenclator.config.OutputTemplateConfig` instances.

    :param token_mapping: Mapping regrouping resolved token values associated
        with their name.

    :return: Tuple of :class:`OutputContext` instances.

    """
    mapping = {config.id: config for config in template_configs}
    destinations = tuple(sorted(mapping.keys()))

    _contexts = []

    for _context in contexts:
        if not len(destinations):
            # noinspection PyProtectedMember
            _context = _context._replace(
                path="",
                destination="",
                destinations=tuple(),
                error=_update_output_error()
            )
            _contexts.append(_context)
            continue

        destination = _context.destination
        config = mapping.get(destination)

        if config is None:
            destination = destinations[0]
            config = mapping.get(destination)

        # Update token values.
        _token_mapping = copy.deepcopy(token_mapping)
        _token_mapping.update({
            "colorspace": _context.colorspace,
            "passname": _context.passname,
        })

        try:
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

        except Exception as exception:
            # noinspection PyProtectedMember
            _context = _context._replace(
                path="",
                destination=destination,
                destinations=destinations,
                error=_update_output_error(error=(config, exception))
            )
            _contexts.append(_context)

        else:
            # noinspection PyProtectedMember
            _context = _context._replace(
                path=os.path.join(path, name),
                destination=destination,
                destinations=destinations,
                error=None
            )
            _contexts.append(_context)

    return tuple(_contexts)


def _update_error(context, error=None):
    """Return error mapping for *context*."""
    if error is not None:
        config, exception = error
        message = "Template configuration contains an error [{}]".format(config.id)
        return {
            "message": message,
            "details": (
                "Impossible to generate a scene name due to the following "
                "error: {}".format(exception)
            )
        }

    if not len(context.template_configs):
        return {
            "message": "No template configurations found.",
            "detail": (
                "You must set at least one template configuration "
                "to generate names.\n"
                "Please read the documentation at "
                "http://nomenclator-nuke.readthedocs.io/en/stable/\n"
            )
        }

    # If no path is set, do not return any error mapping.
    if not len(context.location_path):
        return None

    path = [config.pattern_path for config in context.template_configs]
    return {
        "message": "No matching template configuration found.",
        "details": (
            "Available template paths are:\n"
            "* {}\n".format("\n* ".join(path))
        )
    }


def _update_output_error(error=None):
    """Return error mapping for output *context*."""
    if error is not None:
        config, exception = error
        message = "Output Template configuration contains an error [{}]".format(config.id)
        return {
            "message": message,
            "details": (
                "Impossible to generate an output name due to the following "
                "error: {}".format(exception)
            )
        }

    return {
        "message": "No output template configurations found.",
        "detail": (
            "You must set at least one output template "
            "configuration to generate names.\n"
            "Please read the documentation at "
            "http://nomenclator-nuke.readthedocs.io/en/stable/\n"
        )
    }
