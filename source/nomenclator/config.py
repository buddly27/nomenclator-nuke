# -*- coding: utf-8 -*-

import os
import collections
import getpass

import nomenclator.vendor.toml as toml
from nomenclator.symbol import (
    CONFIG_FILE_NAME,
    DEFAULT_EXPRESSION,
    DEFAULT_MATCH_START,
    DEFAULT_MATCH_END,
    DEFAULT_DESCRIPTIONS,
    DEFAULT_COLORSPACE_ALIASES,
    DEFAULT_CREATE_SUBFOLDERS,
    DEFAULT_MAX_LOCATIONS,
    DEFAULT_MAX_PADDING,
)


#: Configuration Structure type.
Config = collections.namedtuple(
    "Config", [
        "descriptions",
        "default_description",
        "create_subfolders",
        "comp_template_configs",
        "project_template_configs",
        "colorspace_aliases",
        "tokens",
        "max_locations",
        "max_padding",
        "default_padding",
        "username",
        "username_is_default",
    ]
)


#: Template Structure type.
TemplateConfig = collections.namedtuple(
    "TemplateConfig", [
        "id",
        "pattern_path",
        "pattern_base",
        "default_expression",
        "match_start",
        "match_end",
        "append_username_to_name",
        "outputs",
    ]
)


#: Output Template Structure type.
OutputTemplateConfig = collections.namedtuple(
    "OutputTemplateConfig", [
        "id",
        "pattern_path",
        "pattern_base",
        "append_username_to_name",
        "append_colorspace_to_name",
        "append_passname_to_name",
        "append_passname_to_subfolder",
    ]
)


def path():
    """Return path to configuration file.

    The configuration file is returned from the :envvar:`NOMENCLATOR_CONFIG_PATH`
    environment variable, or from the :file:`~/.nuke` folder.

    """
    personal_path = os.path.join(os.path.expanduser("~"), ".nuke")
    return os.path.join(os.getenv("NOMENCLATOR_CONFIG_PATH", personal_path), CONFIG_FILE_NAME)


def fetch():
    """Return configuration object."""
    config_path = path()

    data = {}

    if os.path.exists(config_path):
        with open(config_path, "r") as stream:
            data = toml.load(stream)

    return load(data)


def save(config):
    """Save *config* as a configuration file."""
    data = dump(config)

    with open(path(), "w") as stream:
        toml.dump(data, stream)


def dump(config):
    """Return data mapping from *config* object."""
    data = collections.OrderedDict()

    if config.descriptions != DEFAULT_DESCRIPTIONS:
        data["descriptions"] = config.descriptions

    if config.default_description is not None:
        data["default-description"] = config.default_description

    if config.create_subfolders != DEFAULT_CREATE_SUBFOLDERS:
        data["create-subfolders"] = config.create_subfolders

    if config.colorspace_aliases != DEFAULT_COLORSPACE_ALIASES:
        data["colorspace-aliases"] = collections.OrderedDict(
            config.colorspace_aliases
        )

    if len(config.tokens):
        data["tokens"] = collections.OrderedDict(config.tokens)

    if config.max_locations != DEFAULT_MAX_LOCATIONS:
        data["max-locations"] = config.max_locations

    if config.max_padding != DEFAULT_MAX_PADDING:
        data["max-padding"] = config.max_padding

    if config.default_padding is not None:
        data["default-padding"] = config.default_padding

    if config.username_is_default is False:
        data["username"] = config.username

    if len(config.comp_template_configs) > 0:
        data["comp-templates"] = dump_template_configs(
            config.comp_template_configs,
            include_outputs=True
        )

    if len(config.project_template_configs) > 0:
        data["project-templates"] = dump_template_configs(
            config.project_template_configs
        )

    return data


def dump_template_configs(configs, include_outputs=False):
    """Return data mapping from list of template configs."""
    items = []

    for config in configs:
        data = collections.OrderedDict()
        data["id"] = config.id
        data["pattern-path"] = config.pattern_path
        data["pattern-base"] = config.pattern_base

        if config.default_expression != DEFAULT_EXPRESSION:
            data["default-expression"] = config.default_expression

        if config.match_start != DEFAULT_MATCH_START:
            data["match-start"] = config.match_start

        if config.match_end != DEFAULT_MATCH_END:
            data["match-end"] = config.match_end

        if config.append_username_to_name is not False:
            data["append-username-to-name"] = config.append_username_to_name

        if include_outputs:
            data["outputs"] = dump_output_template_configs(config.outputs)

        items.append(data)

    return items


def dump_output_template_configs(configs):
    """Return data mapping from list of output template configs."""
    items = []

    for config in configs:
        data = collections.OrderedDict()
        data["id"] = config.id
        data["pattern-path"] = config.pattern_path
        data["pattern-base"] = config.pattern_base

        if config.append_username_to_name is not False:
            data["append-username-to-name"] = config.append_username_to_name

        if config.append_colorspace_to_name is not False:
            data["append-colorspace-to-name"] = config.append_colorspace_to_name

        if config.append_passname_to_name is not False:
            data["append-passname-to-name"] = config.append_passname_to_name

        if config.append_passname_to_subfolder is not False:
            data["append-passname-to-subfolder"] = config.append_passname_to_subfolder
        items.append(data)

    return items


def load(data):
    """Return config object from *data* mapping."""
    comp_template_configs = load_template_configs(
        data.get("comp-templates", []),
        include_outputs=True
    )

    project_template_configs = load_template_configs(
        data.get("project-templates", [])
    )

    if data.get("colorspace-aliases") is not None:
        colorspace_aliases = sorted(data["colorspace-aliases"].items())
    else:
        colorspace_aliases = DEFAULT_COLORSPACE_ALIASES

    if data.get("tokens") is not None:
        tokens = sorted(data["tokens"].items())
    else:
        tokens = []

    return Config(
        descriptions=tuple(data.get("descriptions", DEFAULT_DESCRIPTIONS)),
        default_description=data.get("default-description"),
        create_subfolders=data.get("create-subfolders", DEFAULT_CREATE_SUBFOLDERS),
        comp_template_configs=comp_template_configs,
        project_template_configs=project_template_configs,
        colorspace_aliases=tuple(colorspace_aliases),
        tokens=tuple(tokens),
        max_locations=data.get("max-locations", DEFAULT_MAX_LOCATIONS),
        max_padding=data.get("max-padding", DEFAULT_MAX_PADDING),
        default_padding=data.get("default-padding"),
        username=data.get("username", getpass.getuser()),
        username_is_default=data.get("username") is None
    )


def load_template_configs(items, include_outputs=False):
    """Return list of template configs from *items*."""
    templates = []

    for item in items:
        outputs = None

        if include_outputs:
            outputs = load_output_template_configs(item.get("outputs", []))

        template = TemplateConfig(
            id=item["id"],
            pattern_path=item.get("pattern-path", ""),
            pattern_base=item.get("pattern-base", ""),
            default_expression=item.get("default-expression", DEFAULT_EXPRESSION),
            match_start=item.get("match-start", DEFAULT_MATCH_START),
            match_end=item.get("match-end", DEFAULT_MATCH_END),
            append_username_to_name=item.get("append-username-to-name", False),
            outputs=outputs
        )
        templates.append(template)

    return tuple(templates)


def load_output_template_configs(items):
    """Return list of output template configs from *items*."""
    templates = []

    for item in items:
        template = OutputTemplateConfig(
            id=item["id"],
            pattern_path=item.get("pattern-path", ""),
            pattern_base=item.get("pattern-base", ""),
            append_username_to_name=item.get("append-username-to-name", False),
            append_colorspace_to_name=item.get("append-colorspace-to-name", False),
            append_passname_to_name=item.get("append-passname-to-name", False),
            append_passname_to_subfolder=item.get("append-passname-to-subfolder", False),
        )
        templates.append(template)

    return tuple(templates)
