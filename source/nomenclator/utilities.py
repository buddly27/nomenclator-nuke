# -*- coding: utf-8 -*-

import copy
import os

import nuke

from nomenclator.symbol import OUTPUT_CLASSES
import nomenclator.template


def fetch_next_version(path, pattern, token_mapping):
    """Fetch next version from scene files saved in *path*."""
    next_version = 1

    # Ignore version token when resolving base pattern
    _mapping = copy.deepcopy(token_mapping)
    _mapping["version"] = r"{version:\d+}"

    # Generate expected base name pattern from resolved tokens.
    pattern = nomenclator.template.resolve(pattern, _mapping)

    for file_name in os.listdir(path):
        data = nomenclator.template.fetch_resolved_tokens(
            file_name, pattern, match_start=True, match_end=False
        )
        if data is None:
            continue

        previous_version = int(data.get("version", 0))
        next_version = max(next_version, previous_version + 1)

    return next_version


def fetch_nodes():
    """Return a tuple with a list of output nodes and a list all node names."""
    nodes = []
    all_names = []

    for node in nuke.allNodes(group=nuke.root()):
        if node.Class() in OUTPUT_CLASSES:
            nodes.append(node)

        all_names.append(node.name())

    return nodes, all_names


def fetch_recent_comp_paths(max_values=10):
    """Return list of paths recently used to save a composition."""
    paths = []

    try:
        for index in range(1, max_values + 1):
            path = os.path.dirname(nuke.recentFile(index))
            if path not in paths:
                paths.append(path)
    except RuntimeError:
        pass

    return paths


def fetch_paddings(max_value=5):
    """Return all available paddings if notation requested."""
    available = {
        "Hashes (#)": [
            "#" * (index + 1)
            for index in range(max_value)
        ],
        "Printf Notation (%d)": [
            "%{0:02}d".format(index + 1)
            for index in range(max_value)
        ]
    }

    try:
        preferences = nuke.toNode("preferences")
        notation = preferences["UISequenceDisplayMode"].value()
        return available[notation]

    except (TypeError, NameError, KeyError):
        return available["Hashes (#)"]
