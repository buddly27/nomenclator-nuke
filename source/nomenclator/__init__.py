# -*- coding: utf-8 -*-

import nuke

import nomenclator.config
import nomenclator.utilities
from nomenclator.dialog import CompoManagerDialog
from nomenclator.dialog import SettingsDialog

from ._version import __version__


def open_comp_manager_dialog():
    """Open the dialog to manage composition script and render output paths.
    """
    config = nomenclator.config.fetch()
    context = nomenclator.utilities.fetch_output_context(config)
    recent_locations = nomenclator.utilities.fetch_recent_comp_paths(
        max_values=config.max_locations
    )

    panel = CompoManagerDialog(recent_locations, context, config)
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

    if not panel.exec_():
        return

    try:
        nomenclator.config.save(panel.config)
    except Exception as error:
        nuke.critical("Impossible to save config: {}".format(error))
