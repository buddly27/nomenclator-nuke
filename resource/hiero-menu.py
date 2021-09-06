# -*- coding: utf-8 -*-

import hiero.ui

import nomenclator
from nomenclator.vendor.Qt import QtWidgets


parent = hiero.ui.mainWindow()

action1 = QtWidgets.QAction("Nomenclator - Manage Project...", parent)
action1.triggered.connect(nomenclator.open_project_manager_dialog)

action2 = QtWidgets.QAction("Nomenclator - Settings...", parent)
action2.triggered.connect(nomenclator.open_settings_dialog)

target_action = hiero.ui.findMenuAction("foundry.menu.file")
menu = target_action.menu()
separator = menu.insertSeparator(menu.actions()[0])
menu.insertActions(separator, [action1, action2])
