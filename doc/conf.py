# -*- coding: utf-8 -*-

"""Nomenclator Nuke documentation build configuration file."""

import os
import sys
import re

# -- General ------------------------------------------------------------------

# Inject source onto path so that autodoc can find it by default, but in such a
# way as to allow overriding location.
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "source"))
)

# Extensions.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "lowdown"
]

# The suffix of source filenames.
source_suffix = ".rst"

# The master toctree document.
master_doc = "index"

# General information about the project.
project = u"Nomenclator Nuke"
copyright = u"2021, Jeremy Retailleau"

# Version
with open(
    os.path.join(
        os.path.dirname(__file__), "..", "source",
        "nomenclator", "_version.py"
    )
) as _version_file:
    _version = re.match(
        r".*__version__ = \"(.*?)\"", _version_file.read(), re.DOTALL
    ).group(1)

version = _version
release = _version

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ["_template"]

# A list of prefixes to ignore for module listings.
modindex_common_prefix = [
    "nomenclator."
]


# -- HTML output --------------------------------------------------------------

html_theme = "sphinx_rtd_theme"

html_static_path = ["_static"]

# If True, copy source rst files to output for reference.
html_copy_source = True


# -- Autodoc ------------------------------------------------------------------

autodoc_default_options = {
    "members": None,
    "undoc-members": None,
    "inherited-members": None,
    "show-inheritance": None,
}

autodoc_member_order = "bysource"
autodoc_mock_imports = ["nuke", "hiero.core", "hiero.ui", "nomenclator.vendor.Qt"]


def autodoc_skip(app, what, name, obj, skip, options):
    """Don"t skip __init__ method for autodoc."""
    if name == "__init__":
        return False

    return skip


# -- Intersphinx --------------------------------------------------------------

intersphinx_mapping = {
    "python": ("http://docs.python.org/", None),
}


# -- Setup --------------------------------------------------------------------

def setup(app):
    app.connect("autodoc-skip-member", autodoc_skip)
