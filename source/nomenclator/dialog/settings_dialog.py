# -*- coding: utf-8 -*-

from nomenclator.vendor.Qt import QtWidgets, QtCore, QtGui
from nomenclator.widget import EditableList
from nomenclator.widget import EditableTabWidget
from nomenclator.config import CompTemplate, Template

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

    @property
    def config(self):
        """Return updated config."""
        return self._config

    def set_values(self, config):
        """Initialize values."""
        self._tab_widget.widget(0).set_values(config)
        self._tab_widget.widget(1).set_values(config)
        self._tab_widget.widget(2).set_values(config)
        self._tab_widget.widget(3).set_values(config)

    def _setup_ui(self):
        """Initialize user interface."""
        self.setWindowTitle("Nomenclator - Settings")
        self.resize(QtCore.QSize(900, 500))

        self.setStyleSheet(classic_style())

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(5)

        self._tab_widget = QtWidgets.QTabWidget(self)
        self._tab_widget.addTab(GlobalSettingsForm(), "Global")
        self._tab_widget.addTab(CompSettingsForm(), "Comp (.nk)")
        self._tab_widget.addTab(ProjectSettingsForm(), "Project (.hrox)")
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
        self._tab_widget.widget(0).updated.connect(self._update_config)
        self._tab_widget.widget(1).updated.connect(self._update_config)
        self._tab_widget.widget(2).updated.connect(self._update_config)
        self._tab_widget.widget(3).updated.connect(self._update_config)

        self._button_box.clicked.connect(self._button_clicked)

    def _update_config(self, key, value):
        """Update config object from *key* and *value*."""
        # noinspection PyProtectedMember
        self._config = self._config._replace(**{key: value})
        self._update_buttons_states()

    def _button_clicked(self, button):
        """Modify the state of the dialog depending on the button clicked."""
        mapping = {
            "Apply": self._button_box.button(QtWidgets.QDialogButtonBox.Apply),
            "Cancel": self._button_box.button(QtWidgets.QDialogButtonBox.Cancel),
            "Reset": self._button_box.button(QtWidgets.QDialogButtonBox.Reset),
        }

        if button == mapping["Apply"]:
            self.accept()

        elif button == mapping["Cancel"]:
            self.reject()

        elif button == mapping["Reset"]:
            self._config = self._initial_config
            self.set_values(self._config)
            self._update_buttons_states()

    def _update_buttons_states(self):
        """Modify the state of the buttons depending on the config state."""
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
        self._descriptions.blockSignals(True)
        self._descriptions.set_values(config.descriptions)
        self._descriptions.blockSignals(False)

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
        self._descriptions.updated.connect(
            lambda values: self.updated.emit("descriptions", tuple(values))
        )
        self._create_subfolders.stateChanged.connect(
            lambda state: self.updated.emit("create_subfolders", state == QtCore.Qt.Checked)
        )


class CompSettingsForm(QtWidgets.QWidget):
    """Form to manage comp settings."""

    #: :term:`Qt Signal` emitted when a key of the config has changed.
    updated = QtCore.Signal(str, object)

    def __init__(self, parent=None):
        """Initiate the widget."""
        super(CompSettingsForm, self).__init__(parent)
        self._setup_ui()
        self._connect_signals()

        self._templates = []

    def set_values(self, config):
        """Initialize values."""
        self._tab_widget.blockSignals(True)

        self._tab_widget.clear()

        for template in config.comp_templates:
            widget = _CompTemplateForm()
            widget.set_template(template)
            self._tab_widget.addTab(widget, template.id)
            self._templates.append(template)

        self._tab_widget.blockSignals(False)

    def _setup_ui(self):
        """Initialize user interface."""
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(10, 20, 10, 10)
        main_layout.setSpacing(15)

        self._tab_widget = EditableTabWidget(self)
        self._tab_widget.set_instruction(
            "Add naming convention for Nuke composition scripts and\n"
            "render outputs by clicking the '+' button on the top-right corner."
        )
        main_layout.addWidget(self._tab_widget)

    def _connect_signals(self):
        """Initialize signals connection."""
        self._tab_widget.new_tab_requested.connect(self._add_template)
        self._tab_widget.tab_removed.connect(self._template_removed)
        self._tab_widget.tab_edited.connect(self._template_updated)

    def _add_template(self):
        """Add a new tab for template."""
        index = self._tab_widget.count()
        name = "Comp{}".format(index + 1)

        widget = _CompTemplateForm()
        widget.updated.connect(lambda: self._template_updated(index))
        self._templates.append(widget.template())

        self._tab_widget.addTab(widget, name)
        self._tab_widget.setCurrentWidget(widget)

        self.updated.emit("comp_templates", tuple(self._templates))

    def _template_removed(self, index):
        """Remove template at *index* position."""
        del self._templates[index]
        self.updated.emit("comp_templates", tuple(self._templates))

    def _template_updated(self, index):
        """Update template at *index* position."""
        widget = self._tab_widget.widget(index)
        self._templates[index] = widget.template()
        self.updated.emit("comp_templates", tuple(self._templates))


class ProjectSettingsForm(QtWidgets.QWidget):
    """Form to manage project settings."""

    #: :term:`Qt Signal` emitted when a key of the config has changed.
    updated = QtCore.Signal(str, object)

    def __init__(self, parent=None):
        """Initiate the widget."""
        super(ProjectSettingsForm, self).__init__(parent)
        self._setup_ui()
        self._connect_signals()

        self._templates = []

    def set_values(self, config):
        """Initialize values."""
        self._tab_widget.blockSignals(True)

        self._tab_widget.clear()

        for template in config.project_templates:
            widget = _ProjectTemplateForm()
            widget.set_template(template)
            self._tab_widget.addTab(widget, template.id)
            self._templates.append(template)

        self._tab_widget.blockSignals(False)

    def _setup_ui(self):
        """Initialize user interface."""
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(10, 20, 10, 10)
        main_layout.setSpacing(15)

        self._tab_widget = EditableTabWidget(self)
        self._tab_widget.set_instruction(
            "Add naming convention for Nuke Studio or Hiero projects\n"
            "by clicking the '+' button on the top-right corner."
        )
        main_layout.addWidget(self._tab_widget)

    def _connect_signals(self):
        """Initialize signals connection."""
        self._tab_widget.new_tab_requested.connect(self._add_template)
        self._tab_widget.tab_removed.connect(self._template_removed)
        self._tab_widget.tab_edited.connect(self._template_updated)

    def _add_template(self):
        """Add a new tab for template."""
        index = self._tab_widget.count()
        name = "Project{}".format(index + 1)

        widget = _ProjectTemplateForm()
        widget.updated.connect(lambda: self._template_updated(index))
        self._templates.append(widget.template())

        self._tab_widget.addTab(widget, name)
        self._tab_widget.setCurrentWidget(widget)

        self.updated.emit("project_templates", tuple(self._templates))

    def _template_removed(self, index):
        """Remove template at *index* position."""
        del self._templates[index]
        self.updated.emit("project_templates", tuple(self._templates))

    def _template_updated(self, index):
        """Update template at *index* position."""
        widget = self._tab_widget.widget(index)
        self._templates[index] = widget.template()
        self.updated.emit("project_templates", tuple(self._templates))


class _CompTemplateForm(QtWidgets.QWidget):
    """Form to manage comp template settings."""

    #: :term:`Qt Signal` emitted when the template is updated.
    updated = QtCore.Signal()

    def __init__(self, parent=None):
        """Initiate the widget."""
        super(_CompTemplateForm, self).__init__(parent)
        self._setup_ui()
        self._connect_signals()

        self._template = CompTemplate(id="", path="", base_name="", outputs=[])
        self._output_templates = []

    def template(self):
        """Return template object."""
        return self._template

    def set_template(self, template):
        """Initialize values."""
        self._template_form.blockSignals(True)
        self._template_form.initiate(template)
        self._template_form.blockSignals(False)

        self._template = template

        self._tab_widget.blockSignals(True)

        self._tab_widget.clear()

        for index, template in enumerate(template.outputs):
            widget = _OutputTemplateForm()
            widget.set_template(template)
            widget.updated.connect(lambda: self._output_template_updated(index))

            self._tab_widget.addTab(widget, template.id)
            self._output_templates.append(template)

        self._tab_widget.blockSignals(False)

    def _setup_ui(self):
        """Initialize user interface."""
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(10, 20, 10, 10)
        main_layout.setSpacing(15)

        self._template_form = _TemplateForm(self)
        main_layout.addWidget(self._template_form)

        self._tab_widget = EditableTabWidget(self)
        self._tab_widget.set_instruction(
            "Add naming convention for render outputs by clicking\n"
            "the '+' button on the top-right corner."
        )
        main_layout.addWidget(self._tab_widget)

    def _connect_signals(self):
        """Initialize signals connection."""
        self._template_form.updated.connect(self._update_template)
        self._tab_widget.new_tab_requested.connect(self._add_output_template)
        self._tab_widget.tab_removed.connect(self._output_template_removed)
        self._tab_widget.tab_edited.connect(self._output_template_updated)

    def _add_output_template(self):
        """Add a new tab for output template."""
        index = self._tab_widget.count()
        name = "Output{}".format(index + 1)

        widget = _OutputTemplateForm()
        widget.updated.connect(lambda: self._output_template_updated(index))
        self._output_templates.append(widget.template())

        self._tab_widget.addTab(widget, name)
        self._tab_widget.setCurrentWidget(widget)

        self._update_template("outputs", self._output_templates)

    def _output_template_removed(self, index):
        """Remove output template at *index* position."""
        del self._output_templates[index]
        self._update_template("outputs", self._output_templates)

    def _output_template_updated(self, index):
        """Update output template at *index* position."""
        widget = self._tab_widget.widget(index)
        self._output_templates[index] = widget.template()
        self._update_template("outputs", self._output_templates)

    def _update_template(self, key, value):
        """Update comp template object from *key* and *value*."""
        # noinspection PyProtectedMember
        self._template = self._template._replace(**{key: value})

        self.updated.emit()


class _ProjectTemplateForm(QtWidgets.QWidget):
    """Form to manage project template settings."""

    #: :term:`Qt Signal` emitted when the template is updated.
    updated = QtCore.Signal()

    def __init__(self, parent=None):
        """Initiate the widget."""
        super(_ProjectTemplateForm, self).__init__(parent)
        self._setup_ui()
        self._connect_signals()

        self._template = Template(id="", path="", base_name="")

    def template(self):
        """Return template object."""
        return self._template

    def set_template(self, template):
        """Initialize values."""
        self._template_form.blockSignals(True)
        self._template_form.initiate(template)
        self._template_form.blockSignals(False)

        self._template = template

    def _setup_ui(self):
        """Initialize user interface."""
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(10, 20, 10, 10)
        main_layout.setSpacing(15)

        self._template_form = _TemplateForm(self)
        main_layout.addWidget(self._template_form)

        spacer_v = QtWidgets.QSpacerItem(
            0, 0, QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Expanding
        )
        main_layout.addItem(spacer_v)

    def _connect_signals(self):
        """Initialize signals connection."""
        self._template_form.updated.connect(self._update_template)

    def _update_template(self, key, value):
        """Update comp template object from *key* and *value*."""
        # noinspection PyProtectedMember
        self._template = self._template._replace(**{key: value})

        self.updated.emit()


class _OutputTemplateForm(QtWidgets.QWidget):
    """Form to manage output template settings."""

    #: :term:`Qt Signal` emitted when the template is updated.
    updated = QtCore.Signal()

    def __init__(self, parent=None):
        """Initiate the widget."""
        super(_OutputTemplateForm, self).__init__(parent)
        self._setup_ui()
        self._connect_signals()

        self._template = Template(id="", path="", base_name="")

    def template(self):
        """Return template object."""
        return self._template

    def set_template(self, template):
        """Initialize values."""
        self._template_form.blockSignals(True)
        self._template_form.initiate(template)
        self._template_form.blockSignals(False)

    def _setup_ui(self):
        """Initialize user interface."""
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(10, 20, 10, 10)
        main_layout.setSpacing(8)

        self._template_form = _TemplateForm(self)
        main_layout.addWidget(self._template_form)

        spacer_v = QtWidgets.QSpacerItem(
            0, 0, QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Expanding
        )
        main_layout.addItem(spacer_v)

    def _connect_signals(self):
        """Initialize signals connection."""
        self._template_form.updated.connect(self._update_template)

    def _update_template(self, key, value):
        """Update comp template object from *key* and *value*."""
        # noinspection PyProtectedMember
        self._template = self._template._replace(**{key: value})

        self.updated.emit()


class _TemplateForm(QtWidgets.QWidget):
    """Form to manage template path and name."""

    #: :term:`Qt Signal` emitted when a key of the template has changed.
    updated = QtCore.Signal(str, object)

    def __init__(self, parent=None):
        """Initiate the widget."""
        super(_TemplateForm, self).__init__(parent)
        self._setup_ui()
        self._connect_signals()

    def initiate(self, template):
        """Initialize values."""
        self._path.blockSignals(True)
        self._path.setText(template.path)
        self._path.blockSignals(False)

        self._name.blockSignals(True)
        self._name.setText(template.base_name)
        self._name.blockSignals(False)

    def _setup_ui(self):
        """Initialize user interface."""
        main_layout = QtWidgets.QGridLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(8)

        path_lbl = QtWidgets.QLabel("Path", self)
        main_layout.addWidget(path_lbl, 0, 0, 1, 1)

        self._path = QtWidgets.QLineEdit(self)
        main_layout.addWidget(self._path, 0, 1, 1, 1)

        name_lbl = QtWidgets.QLabel("Base Name", self)
        main_layout.addWidget(name_lbl, 1, 0, 1, 1)

        self._name = QtWidgets.QLineEdit(self)
        main_layout.addWidget(self._name, 1, 1, 1, 1)

    def _connect_signals(self):
        """Initialize signals connection."""
        self._path.textChanged.connect(lambda v: self.updated.emit("path", v))
        self._name.textChanged.connect(lambda v: self.updated.emit("base_name", v))


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
