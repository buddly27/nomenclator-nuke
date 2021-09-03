# -*- coding: utf-8 -*-

import copy
import os

import nuke

from nomenclator.symbol import OUTPUT_CLASSES, DEFAULT_EXPRESSION
import nomenclator.template


def fetch_next_version(path, pattern, token_mapping):
    """Fetch next version from scene files saved in *path*.

    :param path: Path to fetch scene files from.

    :param pattern: Pattern to compare scene files with.

    :param token_mapping: Mapping regrouping resolved token values associated
        with their name.

    :return: version integer.

    """
    next_version = 1

    # Ignore version token when resolving base pattern
    mapping = copy.deepcopy(token_mapping)
    mapping["version"] = r"{version:\d+}"

    # Generate expected base name pattern from resolved tokens.
    pattern = nomenclator.template.resolve(pattern, mapping)

    for file_name in os.listdir(path):
        data = nomenclator.template.fetch_resolved_tokens(
            file_name, pattern, match_start=True, match_end=False
        )
        if data is None:
            continue

        previous_version = int(data.get("version", 0))
        next_version = max(next_version, previous_version + 1)

    return next_version


def fetch_version(scene_path, pattern, token_mapping):
    """Fetch version from scene path.

    :param scene_path: Path to the scene file to analyze.

    :param pattern: Pattern to compare scene file with.

    :param token_mapping: Mapping regrouping resolved token values associated
        with their name.

    :return: version integer, or None if no version is found.

    """
    # Ignore version token when resolving base pattern
    mapping = copy.deepcopy(token_mapping)
    mapping["version"] = r"{version:\d+}"

    # Generate expected base name pattern from resolved tokens.
    pattern = nomenclator.template.resolve(pattern, mapping)
    data = nomenclator.template.fetch_resolved_tokens(
        os.path.basename(scene_path), pattern,
        match_start=True, match_end=False
    )

    if data is not None:
        return int(data.get("version", 0)) or None


def fetch_template_config(path, template_configs, token_mapping):
    """Return template configuration compatible with *path*.

    Incoming token mapping will be mutated with new token values
    extracted from matching template configuration.

    :param path: Path to extract template configuration from.

    :param template_configs: List of available
        :class:`~nomenclator.config.TemplateConfig` instances

    :param token_mapping: Mapping regrouping resolved token values associated
        with their name. It will be updated with new token found.

    :return: :class:`~nomenclator.config.TemplateConfig` Instance or None.

    """
    for config in template_configs:
        data = nomenclator.template.fetch_resolved_tokens(
            path, config.pattern_path,
            default_expression=config.default_expression,
            match_start=config.match_start,
            match_end=config.match_end,
        )

        if data is not None:
            token_mapping.update(data)
            return config

    return None


def fetch_output_template_config(path, template_configs):
    """Return output template configuration compatible with *path*.

    Incoming token mapping will be mutated with new token values
    extracted from matching template configuration.

    :param path: Path to extract template configuration from.

    :param template_configs: List of available
        :class:`~nomenclator.config.OutputTemplateConfig` instances

    :return: :class:`~nomenclator.config.OutputTemplateConfig`
        Instance or None.

    """
    for config in template_configs:
        data = nomenclator.template.fetch_resolved_tokens(
            path, config.pattern_path,
            default_expression=DEFAULT_EXPRESSION,
            match_start=True,
            match_end=True,
        )

        if data is not None:
            return config

    return None


def fetch_nodes():
    """Fetch all available output nodes in the graph with all node names.

    :return: tuple with a list of output nodes and a list all
        available node names.

    """
    nodes = []
    all_names = []

    for node in nuke.allNodes(group=nuke.root()):
        if node.Class() in OUTPUT_CLASSES:
            nodes.append(node)

        all_names.append(node.name())

    return nodes, all_names


def fetch_recent_comp_paths(max_values=10):
    """Return list of paths recently used to save a composition.

    :param max_values: Maximum number of recent composition paths to
        return

    :return: List of recent composition paths.

    """
    paths = []

    try:
        for index in range(1, max_values + 1):
            path = os.path.dirname(nuke.recentFile(index))
            if path not in paths:
                paths.append(path)
    except RuntimeError:
        pass

    return tuple(paths)


def fetch_recent_project_paths(max_values=10):
    """Return list of paths recently used to save a project.

    :param max_values: Maximum number of recent composition paths to
        return

    :return: List of recent composition paths.

    """
    import hiero.ui

    paths = []

    action_name = "foundry.project.recentprojects"
    action = hiero.ui.findMenuAction(action_name)
    if action is not None:
        action_menu = action.menu()

        if action_menu is not None:
            items = action_menu.actions()
            for index, item in enumerate(items, 1):
                if index > max_values:
                    break

                path = item.text()
                if not os.path.isfile(path):
                    continue

                path = os.path.dirname(path)
                if path not in paths:
                    paths.append(path)

    return tuple(paths)


def fetch_paddings(max_value=5):
    """Return all available paddings if notation requested.

    :param max_value: Maximum padding number to use.

    :return: List of available paddings.

    """
    available = {
        "Hashes (#)": tuple([
            "#" * (index + 1)
            for index in range(max_value)
        ]),
        "Printf Notation (%d)": tuple([
            "%{0:02}d".format(index + 1)
            for index in range(max_value)
        ])
    }

    try:
        preferences = nuke.toNode("preferences")
        notation = preferences["UISequenceDisplayMode"].value()
        return available[notation]

    except (TypeError, NameError, KeyError):
        return available["Hashes (#)"]


def fetch_current_comp_path():
    """Return current composition path.

    :return: Path to current 'nk' file or empty string.

    """
    try:
        return nuke.scriptName()
    except RuntimeError:
        return ""


def fetch_current_project_path():
    """Return current project path.

    :return: Path to current 'hrox' file or empty string.

    """
    import hiero.core

    projects = hiero.core.projects()
    if not len(projects):
        return ""

    return projects[-1].path()


def fetch_output_path(node):
    """Return output path from *node*.

    :param node: :class:`nuke.Node` instance.

    :return: Output path.

    """
    return node["file"].value()


def fetch_colorspace(node, alias_mapping):
    """Return colorspace value from *node*.

    :param node: :class:`nuke.Node` instance.

    :param alias_mapping: Mapping containing alias to replace
        some values.

    :return: Colorspace value, or "none" if *node* does not have
        a 'colorspace' knob.

    """
    knob = node.knob("colorspace")
    if knob is None:
        return "none"

    value = knob.value()
    return alias_mapping.get(value) or value


def fetch_file_type(node, default_value):
    """Return file type from *node*.

    :param node: :class:`nuke.Node` instance.

    :param default_value: Default value to return if no file type
        is set.

    :return: File type value.

    """
    value = node["file_type"].value()
    return value.strip() or default_value


def fetch_file_types(node):
    """Return list of available file types for *node*.

    :param node: :class:`nuke.Node` instance.

    :return: Tuple containing all available file types.

    """
    values = node["file_type"].values()

    # Strip spaces before and after each value.
    values = (value.strip() for value in values)

    # Keep only first part of value and exclude null values.
    values = (value.split()[0] for value in values if len(value))

    return tuple(values)


def has_multiple_views(node):
    """Indicate whether *node* is configured with multiple views.

    :param node: :class:`nuke.Node` instance.

    :return: Boolean value.

    """
    return len(node["views"].value().split()) > 1


def is_enabled(node):
    """Indicate whether *node* is enabled in the graph.

    :param node: :class:`nuke.Node` instance.

    :return: Boolean value.

    """
    return not node["disable"].value()


def save_comp(context):
    """Save comp with path from *context*."""
    try:
        nuke.scriptSaveAs(context.path)
    except RuntimeError:
        # thrown if operation is cancelled by user.
        return


def update_nodes(context):
    """Update nodes in graph from *context*."""
    for _context in context.outputs:
        if not _context.enabled:
            continue

        node = nuke.toNode(str(_context.name))
        node.setName(str(_context.new_name))
        node["file"].setValue(str(_context.path))
        node["file_type"].setValue(str(_context.file_type))
        node["disable"].setValue(not _context.enabled)

        if context.create_subfolders:
            path = os.path.dirname(_context.path)
            if not os.path.isdir(path):
                os.makedirs(path)
