# -*- coding: utf-8 -*-

from nomenclator.vendor.Qt import QtWidgets

from nomenclator.widget import DescriptionSelector
from nomenclator.widget import VersionWidget
from nomenclator.widget import PathWidget


class CompSettingsForm(QtWidgets.QWidget):
    """Form to manage composition settings."""

    def __init__(self, config, parent=None):
        """Initiate the widget."""
        super(CompSettingsForm, self).__init__(parent)
        self._setup_ui(config)
        self._connect_signals()

    def _setup_ui(self, config):
        """Initialize user interface."""
        main_layout = QtWidgets.QGridLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(8)

        self._description_selector = DescriptionSelector(config.descriptions, self)
        main_layout.addWidget(self._description_selector, 0, 0)

        self._append_username = QtWidgets.QCheckBox("Append username to script", self)
        main_layout.addWidget(self._append_username, 1, 0)

        self._script_path = PathWidget(self)
        main_layout.addWidget(self._script_path, 2, 0, 1, 2)

        self._version_widget = VersionWidget(self)
        main_layout.addWidget(self._version_widget, 0, 1, 2, 1)

    def _connect_signals(self):
        """Initialize signals connection."""
