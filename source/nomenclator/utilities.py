# -*- coding: utf-8 -*-

try:
    from collections import abc as collections_abc
except ImportError:  # Python 2.7
    import collections as collections_abc

import nuke

#: Output classes which can be rendered.
OUTPUT_CLASSES = ("Write", "DeepWrite")


class OptionMapping(collections_abc.Mapping):
    """Regroup all options to initiate dialogs."""

    def __init__(self):
        """Initiate options."""
        super(OptionMapping, self).__init__()
        output_nodes, node_names = fetch_outputs_and_names()

        self._mapping = {
            "output_nodes": output_nodes,
            "node_names": node_names,
            "descriptions": fetch_descriptions(),
            "paddings": fetch_paddings()
        }

    @property
    def nodes(self):
        """Return output nodes."""
        return self._mapping["output_nodes"]

    @property
    def node_names(self):
        """Return all node names."""
        return self._mapping["node_names"]

    @property
    def descriptions(self):
        """Return all available descriptions."""
        return self._mapping["descriptions"]

    @property
    def paddings(self):
        """Return all available paddings."""
        return self._mapping["paddings"]

    def __len__(self):
        """Return count of keys."""
        return len(self._mapping)

    def __iter__(self):
        """Iterate over all keys."""
        for key in self._mapping:
            yield key

    def __getitem__(self, key):
        """Return value for *key*."""
        return self._mapping[key]

    def __str__(self):
        """Return string representation."""
        return "{}({!r}, {!r})".format(
            self.__class__.__name__, self.id, self._mapping
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


def fetch_descriptions():
    """Return all available descriptions."""
    return [
        "comp",
        "precomp",
        "roto",
        "cleanup",
    ]


def fetch_paddings():
    """Return all available paddings if notation requested."""
    available = {
        "Hashes (#)": ["#", "##", "###", "####", "#####"],
        "Printf Notation (%d)": ["%01d", "%02d", "%03d", "%04d", "%05d"]
    }

    try:
        preferences = nuke.toNode("preferences")
        notation = preferences["UISequenceDisplayMode"].value()
        return available.get(notation)

    except (TypeError, NameError, KeyError):
        return available.get("Hashes (#)")
