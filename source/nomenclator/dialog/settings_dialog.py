# -*- coding: utf-8 -*-

from nomenclator.vendor.Qt import QtWidgets, QtCore, QtGui
from nomenclator.widget import EditableList

from .theme import classic_style


class SettingsDialog(QtWidgets.QDialog):

    def __init__(self, config, parent=None):
        """Initiate dialog."""
        super(SettingsDialog, self).__init__(parent)
        self._setup_ui()
        self._connect_signals()

        self._initial_config = config
        self._config = config

        self.set_values(self._config)

    def set_values(self, config):
        """Initialize values."""
        self._tab_widget.widget(0).set_values(config)
        self._tab_widget.widget(1).set_values(config)
        self._tab_widget.widget(2).set_values(config)

    def _setup_ui(self):
        """Initialize user interface."""
        self.setWindowTitle("Nomenclator - Settings")
        self.setMinimumWidth(800)

        self.setStyleSheet(classic_style())

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(5)

        self._tab_widget = QtWidgets.QTabWidget(self)
        self._tab_widget.addTab(GlobalSettingsForm(), "Global")
        self._tab_widget.addTab(TemplateSettingsForm(), "Template")
        self._tab_widget.addTab(AdvancedSettingsForm(), "Advanced")

        main_layout.addWidget(self._tab_widget)

        self._button_box = QtWidgets.QDialogButtonBox(self)
        self._button_box.setOrientation(QtCore.Qt.Horizontal)
        self._button_box.addButton(QtWidgets.QDialogButtonBox.Reset)
        self._button_box.addButton(QtWidgets.QDialogButtonBox.Apply)
        self._button_box.addButton(QtWidgets.QDialogButtonBox.Cancel)
        main_layout.addWidget(self._button_box)

        button = self._button_box.button(QtWidgets.QDialogButtonBox.Reset)
        button.setEnabled(False)

        button = self._button_box.button(QtWidgets.QDialogButtonBox.Apply)
        button.setEnabled(False)

    def _connect_signals(self):
        """Initialize signals connection."""
        self._tab_widget.widget(2).updated.connect(self._update_config)

        self._button_box.accepted.connect(self.accept)
        self._button_box.rejected.connect(self.reject)

    def _update_config(self, key, value):
        # noinspection PyProtectedMember
        self._config = self._config._replace(**{key: value})

        button = self._button_box.button(QtWidgets.QDialogButtonBox.Reset)
        button.setEnabled(self._config != self._initial_config)

        button = self._button_box.button(QtWidgets.QDialogButtonBox.Apply)
        button.setEnabled(self._config != self._initial_config)


class GlobalSettingsForm(QtWidgets.QWidget):
    """Form to manage global settings."""

    #: :term:`Qt Signal` emitted when a key of the config has changed.
    updated = QtCore.Signal(str, object)

    def __init__(self, parent=None):
        """Initiate the widget."""
        super(GlobalSettingsForm, self).__init__(parent)
        self._setup_ui()
        self._connect_signals()

    def set_values(self, config):
        """Initialize values."""
        self._descriptions.set_values(config.descriptions)

        self._create_subfolders.blockSignals(True)
        state = QtCore.Qt.Checked if config.create_subfolders else QtCore.Qt.Unchecked
        self._create_subfolders.setCheckState(state)
        self._create_subfolders.blockSignals(False)

    def _setup_ui(self):
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

    def __init__(self, parent=None):
        """Initiate the widget."""
        super(TemplateSettingsForm, self).__init__(parent)
        self._setup_ui()
        self._connect_signals()

    def set_values(self, config):
        """Initialize values."""
        self._root.setText(config.template_root or "")
        self._tab_widget.widget(0).set_values(config.comp_name_templates)
        self._tab_widget.widget(1).set_values(config.project_name_templates)
        self._tab_widget.widget(2).set_values(config.output_path_templates)
        self._tab_widget.widget(3).set_values(config.output_name_templates)

    def _setup_ui(self):
        """Initialize user interface."""
        main_layout = QtWidgets.QGridLayout(self)
        main_layout.setContentsMargins(10, 20, 10, 10)
        main_layout.setSpacing(20)

        root_lbl = QtWidgets.QLabel("Root Path", self)
        main_layout.addWidget(root_lbl, 0, 0, 1, 1)

        self._root = QtWidgets.QLineEdit(self)
        main_layout.addWidget(self._root, 0, 1, 1, 1)

        self._tab_widget = QtWidgets.QTabWidget(self)
        self._tab_widget.addTab(_TemplateList(), "Comp Names (.nk)")
        self._tab_widget.addTab(_TemplateList(), "Project Names (.hrox)")
        self._tab_widget.addTab(_TemplateList(), "Output Paths")
        self._tab_widget.addTab(_TemplateList(), "Output Names")

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

    def set_values(self, templates):
        """Initialize values."""
        self._templates.set_values(templates)

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

    #: :term:`Qt Signal` emitted when a key of the config has changed.
    updated = QtCore.Signal(str, object)

    def __init__(self, parent=None):
        """Initiate the widget."""
        super(AdvancedSettingsForm, self).__init__(parent)
        self._setup_ui()
        self._connect_signals()

    def set_values(self, config):
        """Initialize values."""
        self._max_locations.blockSignals(True)
        self._max_locations.setValue(config.max_locations)
        self._max_locations.blockSignals(False)

        self._max_padding.blockSignals(True)
        self._max_padding.setValue(config.max_padding)
        self._max_padding.blockSignals(False)

        self._username.blockSignals(True)
        self._username.setText(config.username)
        self._username.setEnabled(not config.username_is_default)
        self._username.blockSignals(False)

        self._username_is_default.blockSignals(True)
        state = QtCore.Qt.Checked if config.username_is_default else QtCore.Qt.Unchecked
        self._username_is_default.setCheckState(state)
        self._username_is_default.blockSignals(False)

    def _setup_ui(self):
        """Initialize user interface."""
        main_layout = QtWidgets.QGridLayout(self)
        main_layout.setContentsMargins(10, 20, 10, 10)
        main_layout.setSpacing(8)

        max_locations_lbl = QtWidgets.QLabel("Max Locations", self)
        main_layout.addWidget(max_locations_lbl, 0, 0, 1, 1)

        self._max_locations = QtWidgets.QSpinBox(self)
        main_layout.addWidget(self._max_locations, 0, 1, 1, 1)

        max_padding_lbl = QtWidgets.QLabel("Max Padding", self)
        main_layout.addWidget(max_padding_lbl, 1, 0, 1, 1)

        self._max_padding = QtWidgets.QSpinBox(self)
        main_layout.addWidget(self._max_padding, 1, 1, 1, 1)

        username_lbl = QtWidgets.QLabel("Username", self)
        main_layout.addWidget(username_lbl, 2, 0, 1, 1)

        self._username = QtWidgets.QLineEdit(self)
        main_layout.addWidget(self._username, 2, 1, 1, 1)

        self._username_is_default = QtWidgets.QCheckBox("Default username is used", self)
        main_layout.addWidget(self._username_is_default, 3, 1, 1, 1)

        spacer_v = QtWidgets.QSpacerItem(
            0, 0, QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Expanding
        )
        main_layout.addItem(spacer_v, 4, 1, 1, 1)

    def _connect_signals(self):
        """Initialize signals connection."""
        self._username.textChanged.connect(lambda v: self.updated.emit("username", v))
        self._max_locations.valueChanged.connect(lambda v: self.updated.emit("max_locations", v))
        self._max_padding.valueChanged.connect(lambda v: self.updated.emit("max_padding", v))
        self._username_is_default.stateChanged.connect(self._toggle_username_default)

    def _toggle_username_default(self):
        """Indicate whether the username used is default or not."""
        value = self._username_is_default.isChecked()
        self._username.setEnabled(not value)
        self.updated.emit("username_is_default", value)
