# -*- coding: utf-8 -*-

import nuke

from nomenclator.symbol import OUTPUT_CLASSES


def fetch_outputs_and_names():
    """Return a tuple with a list of output nodes and a list all node names."""
    output_nodes = []
    all_names = []

    for node in nuke.allNodes(group=nuke.root()):
        if node.Class() in OUTPUT_CLASSES:
            output_nodes.append(node)

        all_names.append(node.name())

    return output_nodes, all_names


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
