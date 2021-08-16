# -*- coding: utf-8 -*-

import os
import json
import collections

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
            data = json.load(stream.read())

    return extract(data)


def extract(data):
    """Extract configuration object from *data*."""
    nodes, node_names = nomenclator.utilities.fetch_outputs_and_names()

    paddings = nomenclator.utilities.fetch_paddings(
        max_value=data.get("maximum-padding", 5)
    )

    return Config(
        recent_locations=data.get("recent-locations", []),
        descriptions=tuple(data.get("descriptions", DEFAULT_DESCRIPTIONS)),
        paddings=paddings,
        nodes=nodes,
        node_names=node_names
    )
