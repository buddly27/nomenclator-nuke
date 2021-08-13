# -*- coding: utf-8 -*-

import nuke

import nomenclator.utilities
from nomenclator.dialog import CompoManagerDialog

from ._version import __version__


def open_comp_manager_dialog():
    """Open the dialog to manage composition script and render output paths.
    """
    options = nomenclator.utilities.OptionMapping()
    panel = CompoManagerDialog(options)
    panel.exec_()


def open_project_manager_dialog():
    """Open the dialog to manage project.
    """
    pass


def open_output_manager_dialog():
    """Open the dialog to manage render output paths.
    """
    pass
