# -*- coding: utf-8 -*-

#: Output classes which can be rendered.
OUTPUT_CLASSES = ("Write", "DeepWrite")

#: Name of the configuration file.
CONFIG_FILE_NAME = "nomenclator.toml"

#: Default expression to resolve token if none is specified in a template pattern.
DEFAULT_EXPRESSION = r"[\w_.-]+"

#: Default value for matching the start of a template path pattern.
DEFAULT_MATCH_START = True

#: Default value for matching the end of a template path pattern.
DEFAULT_MATCH_END = True

#: Default description tuples.
DEFAULT_DESCRIPTIONS = ("comp", "precomp", "roto", "cleanup")

#: Default value for creating subfolders on saving.
DEFAULT_CREATE_SUBFOLDERS = False

#: Default maximum recent locations to display.
DEFAULT_MAX_LOCATIONS = 5

#: Default maximum padding to display.
DEFAULT_MAX_PADDING = 5
