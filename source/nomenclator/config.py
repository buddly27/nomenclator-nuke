# -*- coding: utf-8 -*-

import os
import collections
import getpass

import nomenclator.vendor.toml
from nomenclator.symbol import (
    CONFIG_FILE_NAME,
    DEFAULT_DESCRIPTIONS,
    DEFAULT_CREATE_SUBFOLDERS,
    DEFAULT_MAX_LOCATIONS,
    DEFAULT_MAX_PADDING,
)


#: Configuration Structure type.
Config = collections.namedtuple(
    "Config", [
        "descriptions",
        "create_subfolders",
        "template_root",
        "comp_name_templates",
        "project_name_templates",
        "output_path_templates",
        "output_name_templates",
        "max_locations",
        "max_padding",
        "username",
        "username_is_default",
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
            data = nomenclator.vendor.toml.load(stream)

    return extract(data)


def save(config):
    """Save *config* as a configuration file."""
    data = collections.OrderedDict()

    if config.descriptions != DEFAULT_DESCRIPTIONS:
        data["descriptions"] = config.descriptions

    if config.create_subfolders != DEFAULT_CREATE_SUBFOLDERS:
        data["create-subfolders"] = config.create_subfolders

    if config.max_locations != DEFAULT_MAX_LOCATIONS:
        data["max-locations"] = config.max_locations

    if config.max_padding != DEFAULT_MAX_PADDING:
        data["max-padding"] = config.max_padding

    if config.username_is_default is False:
        data["username"] = config.username

    data["template"] = collections.OrderedDict()

    if config.template_root != "":
        data["template"]["root"] = config.template_root

    if len(config.comp_name_templates) > 0:
        data["template"]["comp-names"] = config.comp_name_templates

    if len(config.project_name_templates) > 0:
        data["template"]["project-names"] = config.project_name_templates

    if len(config.output_path_templates) > 0:
        data["template"]["output-paths"] = config.output_path_templates

    if len(config.output_name_templates) > 0:
        data["template"]["output-names"] = config.output_name_templates

    with open(config_path(), "w") as stream:
        nomenclator.vendor.toml.dump(data, stream)


def extract(data):
    """Extract configuration object from Nuke scene and from *data* mapping."""
    template_data = data.get("template", {})

    return Config(
        descriptions=tuple(data.get("descriptions", DEFAULT_DESCRIPTIONS)),
        create_subfolders=data.get("create-subfolders", DEFAULT_CREATE_SUBFOLDERS),
        template_root=template_data.get("root", ""),
        comp_name_templates=tuple(template_data.get("comp-names", [])),
        project_name_templates=tuple(template_data.get("project-names", [])),
        output_path_templates=tuple(template_data.get("output-paths", [])),
        output_name_templates=tuple(template_data.get("output-names", [])),
        max_locations=data.get("max-locations", DEFAULT_MAX_LOCATIONS),
        max_padding=data.get("max-padding", DEFAULT_MAX_PADDING),
        username=data.get("username", getpass.getuser()),
        username_is_default=data.get("username") is None
    )
