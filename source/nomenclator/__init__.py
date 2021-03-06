# -*- coding: utf-8 -*-

import nuke

import nomenclator.config
import nomenclator.context
import nomenclator.utilities
from nomenclator.dialog import CompoManagerDialog
from nomenclator.dialog import OutputsManagerDialog
from nomenclator.dialog import ProjectManagerDialog
from nomenclator.dialog import SettingsDialog

from ._version import __version__


def open_comp_manager_dialog():
    """Open the dialog to manage composition script and render output paths.
    """
    config = nomenclator.config.fetch()
    context = nomenclator.context.fetch(config)

    panel = CompoManagerDialog(context)

    if not panel.exec_():
        return

    context = panel.context
    nomenclator.utilities.update_nodes(context)
    nomenclator.utilities.save_comp(context)


def open_project_manager_dialog():
    """Open the dialog to manage project.
    """
    config = nomenclator.config.fetch()
    context = nomenclator.context.fetch(config, is_project=True)

    panel = ProjectManagerDialog(context)

    if not panel.exec_():
        return

    nomenclator.utilities.save_project(context)


def open_output_manager_dialog():
    """Open the dialog to manage render output paths.
    """
    config = nomenclator.config.fetch()
    context = nomenclator.context.fetch(config)

    panel = OutputsManagerDialog(context)

    if not panel.exec_():
        return

    context = panel.context
    nomenclator.utilities.update_nodes(context)


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
