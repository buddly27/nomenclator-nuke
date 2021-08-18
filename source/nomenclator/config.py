# -*- coding: utf-8 -*-

import os
import collections

import nomenclator.vendor.toml
import nomenclator.utilities
from nomenclator.symbol import CONFIG_FILE_NAME, DEFAULT_DESCRIPTIONS

#: Configuration type.
Config = collections.namedtuple(
    "Config", [
        "recent_locations",
        "descriptions",
        "paddings",
        "nodes",
        "node_names"
    ]
)


def fetch():
    """Return configuration object from personal Nuke folder."""
    path = os.path.join(os.path.expanduser("~"), ".nuke", CONFIG_FILE_NAME)

    data = {}

    if os.path.exists(path):
        with open(path, "r") as stream:
            data = nomenclator.vendor.toml.load(stream.read())

    return extract(data)


def extract(data):
    """Extract configuration object from *data*."""
    nodes, node_names = nomenclator.utilities.fetch_outputs_and_names()

    recent_locations = nomenclator.utilities.fetch_recent_locations(
        max_values=data.get("maximum-recent-locations", 5)
    )
    paddings = nomenclator.utilities.fetch_paddings(
        max_value=data.get("maximum-padding", 5)
    )

    return Config(
        recent_locations=tuple(recent_locations),
        descriptions=tuple(data.get("descriptions", DEFAULT_DESCRIPTIONS)),
        paddings=tuple(paddings),
        nodes=tuple(nodes),
        node_names=tuple(node_names)
    )
