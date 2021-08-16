# -*- coding: utf-8 -*-

from nomenclator.vendor.Qt import QtWidgets, QtCore


class SettingsDialog(QtWidgets.QDialog):

    def __init__(self, config, parent=None):
        super(SettingsDialog, self).__init__(parent)
        self._setup_ui(config)

