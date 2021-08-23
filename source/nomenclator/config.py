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
        "comp_templates",
        "project_templates",
        "max_locations",
        "max_padding",
        "username",
        "username_is_default",
    ]
)


#: Comp Template Structure type.
CompTemplate = collections.namedtuple(
    "CompTemplate", [
        "id",
        "path",
        "base_name",
        "outputs",
    ]
)

#: Template Structure type.
Template = collections.namedtuple(
    "OutputTemplate", [
        "id",
        "path",
        "base_name",
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

    return load(data)


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

    if len(config.comp_templates) > 0:
        data["comp-templates"] = _dump_comp_templates(config.comp_templates)

    if len(config.project_templates) > 0:
        data["project-templates"] = _dump_templates(config.project_templates)

    with open(config_path(), "w") as stream:
        nomenclator.vendor.toml.dump(data, stream)


def _dump_comp_templates(comp_templates):
    """Return data mapping from list of comp templates."""
    items = []

    for template in comp_templates:
        data = collections.OrderedDict()
        data["id"] = template.id
        data["path"] = template.path
        data["base-name"] = template.base_name
        data["outputs"] = _dump_templates(template.outputs)
        items.append(data)

    return items


def _dump_templates(templates):
    """Return data mapping from list of templates."""
    items = []

    for template in templates:
        data = collections.OrderedDict()
        data["id"] = template.id
        data["path"] = template.path
        data["base-name"] = template.base_name
        items.append(data)

    return items


def load(data):
    """Return configuration object from Nuke scene and from *data* mapping."""
    return Config(
        descriptions=tuple(data.get("descriptions", DEFAULT_DESCRIPTIONS)),
        create_subfolders=data.get("create-subfolders", DEFAULT_CREATE_SUBFOLDERS),
        comp_templates=tuple(_load_comp_templates(data.get("comp-templates", []))),
        project_templates=tuple(_load_templates(data.get("project-templates", []))),
        max_locations=data.get("max-locations", DEFAULT_MAX_LOCATIONS),
        max_padding=data.get("max-padding", DEFAULT_MAX_PADDING),
        username=data.get("username", getpass.getuser()),
        username_is_default=data.get("username") is None
    )


def _load_comp_templates(items):
    """Return list of comp templates from *items*."""
    templates = []

    for item in items:
        template = CompTemplate(
            id=item["id"],
            path=item["path"],
            base_name=item["base-name"],
            outputs=tuple(_load_templates(item.get("outputs", [])))
        )
        templates.append(template)

    return templates


def _load_templates(items):
    """Return list of templates from *items*."""
    templates = []

    for item in items:
        template = Template(
            id=item["id"],
            path=item["path"],
            base_name=item["base-name"],
        )
        templates.append(template)

    return templates
