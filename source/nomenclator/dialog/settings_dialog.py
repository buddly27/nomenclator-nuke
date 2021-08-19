# -*- coding: utf-8 -*-

from nomenclator.vendor.Qt import QtWidgets, QtCore
from nomenclator.widget import GroupWidget
from nomenclator.widget import EditableList

from .theme import classic_style


class SettingsDialog(QtWidgets.QDialog):

    def __init__(self, config, parent=None):
        super(SettingsDialog, self).__init__(parent)
        self._setup_ui(config)
        self._connect_signals()

    def _setup_ui(self, config):
        """Initialize user interface."""
        self.setWindowTitle("Nomenclator - Settings")
        self.setMinimumWidth(900)

        self.setStyleSheet(classic_style())

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(5)

        global_settings_form = GlobalSettingsForm(config, self)

        global_settings_group = GroupWidget(global_settings_form, self)
        global_settings_group.setTitle("Global")
        main_layout.addWidget(global_settings_group)

        convention_settings_form = ConventionSettingsForm(config, self)

        convention_settings_group = GroupWidget(convention_settings_form, self)
        convention_settings_group.setTitle("Naming Convention")
        main_layout.addWidget(convention_settings_group)

        self._button_box = QtWidgets.QDialogButtonBox(self)
        self._button_box.setOrientation(QtCore.Qt.Horizontal)
        self._button_box.addButton("Apply", QtWidgets.QDialogButtonBox.AcceptRole)
        self._button_box.addButton("Cancel", QtWidgets.QDialogButtonBox.RejectRole)
        main_layout.addWidget(self._button_box)

    def _connect_signals(self):
        """Initialize signals connection."""
        self._button_box.accepted.connect(self.accept)
        self._button_box.rejected.connect(self.reject)


class GlobalSettingsForm(QtWidgets.QWidget):
    """Form to manage global settings."""

    def __init__(self, config, parent=None):
        """Initiate the widget."""
        super(GlobalSettingsForm, self).__init__(parent)
        self._setup_ui(config)
        self._connect_signals()

    def _setup_ui(self, config):
        """Initialize user interface."""
        main_layout = QtWidgets.QGridLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(8)

        self._create_subfolders = QtWidgets.QCheckBox("Create sub-folders for outputs", self)
        main_layout.addWidget(self._create_subfolders, 0, 0)

    def _connect_signals(self):
        """Initialize signals connection."""


class ConventionSettingsForm(QtWidgets.QWidget):
    """Form to manage naming convention settings."""

    def __init__(self, config, parent=None):
        """Initiate the widget."""
        super(ConventionSettingsForm, self).__init__(parent)
        self._setup_ui(config)
        self._connect_signals()

    def _setup_ui(self, config):
        """Initialize user interface."""
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(8)

        self._tab_widget = QtWidgets.QTabWidget(self)

        comp_widget = TemplateSettingsForm(config)
        self._tab_widget.addTab(comp_widget, "Comp (.nk)")

        project_widget = TemplateSettingsForm(config)
        self._tab_widget.addTab(project_widget, "Project (.hrox)")

        output_widget = TemplateSettingsForm(config)
        self._tab_widget.addTab(output_widget, "Render Outputs")

        main_layout.addWidget(self._tab_widget)

    def _connect_signals(self):
        """Initialize signals connection."""


class TemplateSettingsForm(QtWidgets.QWidget):
    """Form to manage template settings."""

    def __init__(self, config, parent=None):
        """Initiate the widget."""
        super(TemplateSettingsForm, self).__init__(parent)
        self._setup_ui(config)
        self._connect_signals()

    def _setup_ui(self, config):
        """Initialize user interface."""
        main_layout = QtWidgets.QGridLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(8)

        location_lbl = QtWidgets.QLabel("Location Template", self)
        main_layout.addWidget(location_lbl, 0, 0, 1, 1)

        self._location = QtWidgets.QLineEdit(self)
        main_layout.addWidget(self._location, 0, 1, 1, 1)

        spacer = QtWidgets.QSpacerItem(
            10, 10, QtWidgets.QSizePolicy.Fixed,
            QtWidgets.QSizePolicy.Fixed
        )
        main_layout.addItem(spacer, 1, 0, 1, 2)

        name_templates_lbl = QtWidgets.QLabel("Name Templates", self)
        main_layout.addWidget(name_templates_lbl, 2, 0, 1, 2)

        self._name_templates = EditableList(self)
        main_layout.addWidget(self._name_templates, 3, 0, 1, 2)

    def _connect_signals(self):
        """Initialize signals connection."""
