# -*- coding: utf-8 -*-

from nomenclator.vendor.Qt import QtWidgets, QtCore
from nomenclator.widget import LocationWidget
from nomenclator.widget import GroupWidget
from nomenclator.widget import DescriptionSelector
from nomenclator.widget import PathWidget
from nomenclator.widget import VersionWidget
from nomenclator.widget import OutputSettingsForm

from .theme import classic_style


class CompoManagerDialog(QtWidgets.QDialog):

    def __init__(self, recent_locations, paddings, config, parent=None):
        """Initiate dialog."""
        super(CompoManagerDialog, self).__init__(parent)
        self._setup_ui(recent_locations, paddings, config)
        self._connect_signals()

    def set_values(self, nodes, node_names):
        """Initialize values."""
        self._outputs_settings_group.setEnabled(len(nodes) > 0)
        self._output_settings_form.set_values(nodes, node_names)

    def _setup_ui(self, recent_locations, paddings, config):
        """Initialize user interface."""
        self.setWindowTitle("Nomenclator - Composition Manager")
        self.setMinimumWidth(1100)

        self.setStyleSheet(classic_style())

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self._location = LocationWidget(recent_locations, self)
        main_layout.addWidget(self._location)

        body_layout = QtWidgets.QVBoxLayout()
        body_layout.setContentsMargins(10, 10, 10, 10)
        body_layout.setSpacing(8)

        self._comp_settings_form = CompSettingsForm(config, self)

        comp_settings_group = GroupWidget(self._comp_settings_form, self)
        comp_settings_group.setTitle("Composition")
        body_layout.addWidget(comp_settings_group)

        self._output_settings_form = OutputSettingsForm(paddings, self)

        self._outputs_settings_group = GroupWidget(self._output_settings_form, self)
        self._outputs_settings_group.set_vertical_stretch(True)
        self._outputs_settings_group.setTitle("Render Outputs")
        body_layout.addWidget(self._outputs_settings_group)

        self._button_box = QtWidgets.QDialogButtonBox(self)
        self._button_box.setOrientation(QtCore.Qt.Horizontal)
        self._button_box.addButton("Apply", QtWidgets.QDialogButtonBox.AcceptRole)
        self._button_box.addButton("Cancel", QtWidgets.QDialogButtonBox.RejectRole)
        body_layout.addWidget(self._button_box)

        main_layout.addItem(body_layout)

    def _connect_signals(self):
        """Initialize signals connection."""
        self._button_box.accepted.connect(self.accept)
        self._button_box.rejected.connect(self.reject)


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
