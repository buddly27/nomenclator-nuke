# -*- coding: utf-8 -*-

from nomenclator.vendor.Qt import QtWidgets, QtCore
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
        self.setMinimumWidth(800)

        self.setStyleSheet(classic_style())

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(5)

        self._tab_widget = QtWidgets.QTabWidget(self)

        global_settings_form = GlobalSettingsForm(config, self)
        self._tab_widget.addTab(global_settings_form, "Global")

        template_settings_form = TemplateSettingsForm(config, self)
        self._tab_widget.addTab(template_settings_form, "Template")

        advanced_settings_form = AdvancedSettingsForm(config, self)
        self._tab_widget.addTab(advanced_settings_form, "Advanced")

        main_layout.addWidget(self._tab_widget)

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
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(10, 20, 10, 10)
        main_layout.setSpacing(8)

        descriptions_lbl = QtWidgets.QLabel("Descriptions", self)
        main_layout.addWidget(descriptions_lbl)

        self._descriptions = EditableList(self)
        self._descriptions.setMaximumHeight(200)
        main_layout.addWidget(self._descriptions)

        self._create_subfolders = QtWidgets.QCheckBox("Create sub-folders for outputs", self)
        main_layout.addWidget(self._create_subfolders)

        spacer_v = QtWidgets.QSpacerItem(
            0, 0, QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Expanding
        )
        main_layout.addItem(spacer_v)

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
        main_layout.setContentsMargins(10, 20, 10, 10)
        main_layout.setSpacing(20)

        root_lbl = QtWidgets.QLabel("Root Path", self)
        main_layout.addWidget(root_lbl, 0, 0, 1, 1)

        self._root = QtWidgets.QLineEdit(self)
        main_layout.addWidget(self._root, 0, 1, 1, 1)

        self._tab_widget = QtWidgets.QTabWidget(self)

        comp_template = _TemplateList()
        self._tab_widget.addTab(comp_template, "Comp Names (.nk)")

        project_template = _TemplateList()
        self._tab_widget.addTab(project_template, "Project Names (.hrox)")

        destination_template = _TemplateList()
        self._tab_widget.addTab(destination_template, "Output Paths")

        output_template = _TemplateList()
        self._tab_widget.addTab(output_template, "Output Names")

        main_layout.addWidget(self._tab_widget, 1, 0, 1, 2)

    def _connect_signals(self):
        """Initialize signals connection."""


class _TemplateList(QtWidgets.QWidget):
    """Form to manage template lists."""

    def __init__(self, parent=None):
        """Initiate the widget."""
        super(_TemplateList, self).__init__(parent)
        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self):
        """Initialize user interface."""
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(10, 20, 10, 10)
        main_layout.setSpacing(8)

        self._templates = EditableList(self)
        main_layout.addWidget(self._templates)

    def _connect_signals(self):
        """Initialize signals connection."""


class AdvancedSettingsForm(QtWidgets.QWidget):
    """Form to manage advanced settings."""

    def __init__(self, config, parent=None):
        """Initiate the widget."""
        super(AdvancedSettingsForm, self).__init__(parent)
        self._setup_ui(config)
        self._connect_signals()

    def _setup_ui(self, config):
        """Initialize user interface."""
        main_layout = QtWidgets.QGridLayout(self)
        main_layout.setContentsMargins(10, 20, 10, 10)
        main_layout.setSpacing(8)

        username_lbl = QtWidgets.QLabel("Username", self)
        main_layout.addWidget(username_lbl, 0, 0, 1, 1)

        self._username = QtWidgets.QLineEdit(self)
        main_layout.addWidget(self._username, 0, 1, 1, 1)

        max_locations_lbl = QtWidgets.QLabel("Max Locations", self)
        main_layout.addWidget(max_locations_lbl, 1, 0, 1, 1)

        self._max_locations = QtWidgets.QSpinBox(self)
        self._max_locations.setMinimumHeight(25)
        main_layout.addWidget(self._max_locations, 1, 1, 1, 1)

        max_padding_lbl = QtWidgets.QLabel("Max Padding", self)
        main_layout.addWidget(max_padding_lbl, 2, 0, 1, 1)

        self._max_padding = QtWidgets.QSpinBox(self)
        self._max_padding.setMinimumHeight(25)
        main_layout.addWidget(self._max_padding, 2, 1, 1, 1)

        spacer_v = QtWidgets.QSpacerItem(
            0, 0, QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Expanding
        )
        main_layout.addItem(spacer_v, 3, 1, 1, 1)

    def _connect_signals(self):
        """Initialize signals connection."""
