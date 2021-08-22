# -*- coding: utf-8 -*-

import nomenclator.config
from nomenclator.dialog import CompoManagerDialog
from nomenclator.dialog import SettingsDialog

from ._version import __version__


def open_comp_manager_dialog():
    """Open the dialog to manage composition script and render output paths.
    """
    config = nomenclator.config.fetch()
    panel = CompoManagerDialog(config)
    panel.exec_()


def open_project_manager_dialog():
    """Open the dialog to manage project.
    """
    pass


def open_output_manager_dialog():
    """Open the dialog to manage render output paths.
    """
    pass


def open_settings_dialog():
    """Open the dialog to manage settings.
    """
    config = nomenclator.config.fetch()
    panel = SettingsDialog(config)

    if panel.exec_():
        nomenclator.config.save(panel.config)
