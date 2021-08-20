# -*- coding: utf-8 -*-

import os
import collections

import nomenclator.vendor.toml
from nomenclator.symbol import CONFIG_FILE_NAME, DEFAULT_DESCRIPTIONS


#: Configuration Structure type.
Config = collections.namedtuple(
    "Config", [
        "max_recent_locations",
        "max_padding",
        "descriptions",
        "template_root",
        "comp_name_templates",
        "project_name_templates",
        "output_path_templates",
        "output_name_templates",
    ]
)


def config_path():
    """Return path to configuration file.

    The configuration file is returned from the :envvar:`NOMENCLATURE_CONFIG_PATH`
    environment variable, or from the :file:`~/.nuke` folder.

    """
    personal_path = os.path.join(os.path.expanduser("~"), ".nuke")
    return os.path.join(os.getenv("NOMENCLATURE_CONFIG_PATH", personal_path), CONFIG_FILE_NAME)


def fetch():
    """Return configuration object from personal Nuke folder."""
    path = config_path()

    data = {}

    if os.path.exists(path):
        with open(path, "r") as stream:
            data = nomenclator.vendor.toml.load(stream.read())

    return extract(data)


def extract(data):
    """Extract configuration object from Nuke scene and from *data* mapping."""
    template_data = data.get("template", {})

    return Config(
        max_recent_locations=data.get("maximum-recent-locations", 5),
        max_padding=data.get("maximum-padding", 5),
        descriptions=tuple(data.get("descriptions", DEFAULT_DESCRIPTIONS)),
        template_root=template_data.get("root"),
        comp_name_templates=tuple(template_data.get("comp-names", [])),
        project_name_templates=tuple(template_data.get("project-names", [])),
        output_path_templates=tuple(template_data.get("output-paths", [])),
        output_name_templates=tuple(template_data.get("output-names", [])),
    )
