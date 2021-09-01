# -*- coding: utf-8 -*-

import copy
import os

import nuke

from nomenclator.symbol import OUTPUT_CLASSES
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
