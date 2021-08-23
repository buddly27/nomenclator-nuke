# -*- coding: utf-8 -*-

import os
import collections

import nuke

from nomenclator.symbol import OUTPUT_CLASSES


#: Configuration Structure type.
CompContext = collections.namedtuple(
    "CompContext", [
        "recent_locations",
        "output",
    ]
)


#: Configuration Structure type.
OutputContext = collections.namedtuple(
    "OutputContext", [
        "nodes",
        "node_names",
        "paddings"
    ]
)


#: Configuration Structure type.
ProjectContext = collections.namedtuple(
    "ProjectContext", [
        "recent_locations",
    ]
)


def fetch_comp(config):
    """Fetch context for comp management."""
    return CompContext(
        recent_locations=fetch_recent_locations(max_values=config.max_locations),
        output=fetch_output(config)
    )


def fetch_output(config):
    """Fetch context for render outputs management."""
    nodes, node_names = fetch_outputs_and_names()

    return OutputContext(
        nodes=nodes,
        node_names=node_names,
        paddings=fetch_paddings(max_value=config.max_padding)
    )


def fetch_project(config):
    """Fetch context for project management."""
    return ProjectContext(
        recent_locations=fetch_recent_locations(max_values=config.max_locations),
    )


def fetch_outputs_and_names():
    """Return a tuple with a list of output nodes and a list all node names."""
    output_nodes = []
    all_names = []

    for node in nuke.allNodes(group=nuke.root()):
        if node.Class() in OUTPUT_CLASSES:
            output_nodes.append(node)

        all_names.append(node.name())

    return output_nodes, all_names


def fetch_recent_locations(max_values=10):
    """Return list of location recently used to save a composition."""
    paths = []

    try:
        for index in range(1, max_values + 1):
            path = os.path.dirname(nuke.recentFile(index))
            if path not in paths:
                paths.append(path)
    except (ValueError, RuntimeError):
        pass

    return paths


def fetch_paddings(max_value):
    """Return all available paddings if notation requested."""
    available = {
        "Hashes (#)": ["#" * (i + 1) for i in range(max_value)],
        "Printf Notation (%d)": ["%{0:02}d".format(i + 1) for i in range(max_value)]
    }

    try:
        preferences = nuke.toNode("preferences")
        notation = preferences["UISequenceDisplayMode"].value()
        return available.get(notation)

    except (TypeError, NameError, KeyError):
        return available.get("Hashes (#)")
