# -*- coding: utf-8 -*-

import os

import nuke

from nomenclator.symbol import OUTPUT_CLASSES


def fetch_output_context(config):
    """Return a mapping with all data needed for output management."""
    nodes, node_names = fetch_nodes()
    paddings = fetch_paddings(max_value=config.max_padding)

    return {
        "nodes": nodes,
        "node_names": node_names,
        "paddings": paddings
    }


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
