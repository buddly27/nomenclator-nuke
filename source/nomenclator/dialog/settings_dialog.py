# -*- coding: utf-8 -*-

from nomenclator.vendor.Qt import QtWidgets, QtCore
from nomenclator.widget import EditableList
from nomenclator.widget import EditableTabWidget
from nomenclator.widget import EditableTable
from nomenclator.config import TemplateConfig, load_template_configs

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
        self._tab_widget.widget(4).set_values(config)
        self._tab_widget.widget(5).set_values(config)

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
        self._tab_widget.addTab(CompSettingsForm(), "Comp Resolvers")
        self._tab_widget.addTab(ProjectSettingsForm(), "Project Resolvers")
        self._tab_widget.addTab(ColorspaceSettingsForm(), "Colorspace")
        self._tab_widget.addTab(TokenSettingsForm(), "Tokens")
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
        self._tab_widget.widget(4).updated.connect(self._update_config)
        self._tab_widget.widget(5).updated.connect(self._update_config)

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
            lambda values: self.updated.emit("descriptions", values)
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

    def templates(self):
        """Return list of templates."""
        templates = []

        for index in range(self._tab_widget.count()):
            widget = self._tab_widget.widget(index)
            identifier = self._tab_widget.tabText(index)
            templates.append(widget.template(identifier))

        return tuple(templates)

    def set_values(self, config):
        """Initialize values."""
        self._tab_widget.clear()

        for _config in config.comp_template_configs:
            widget = _CompTemplateForm()
            widget.set_values(_config)
            widget.updated.connect(self._template_updated)
            self._tab_widget.addTab(widget, _config.id)

    def _setup_ui(self):
        """Initialize user interface."""
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(10, 20, 10, 10)
        main_layout.setSpacing(15)

        self._tab_widget = EditableTabWidget(self)
        self._tab_widget.set_instruction(
            "Add naming convention for Nuke composition scripts (.nk) and\n"
            "render outputs by clicking the '+' button on the top-right corner."
        )
        main_layout.addWidget(self._tab_widget)

    def _connect_signals(self):
        """Initialize signals connection."""
        self._tab_widget.new_tab_requested.connect(self._add_template)
        self._tab_widget.tab_removed.connect(self._template_updated)
        self._tab_widget.tab_edited.connect(self._template_updated)

    def _add_template(self):
        """Add a new tab for template."""
        identifier = "Comp{}".format(self._tab_widget.count() + 1)

        widget = _CompTemplateForm()
        widget.updated.connect(self._template_updated)

        self._tab_widget.addTab(widget, identifier)
        self._tab_widget.setCurrentWidget(widget)

        self._template_updated()

    def _template_updated(self):
        """Emit signal once a template has been updated."""
        self.updated.emit("comp_template_configs", self.templates())


class ProjectSettingsForm(QtWidgets.QWidget):
    """Form to manage project settings."""

    #: :term:`Qt Signal` emitted when a key of the config has changed.
    updated = QtCore.Signal(str, object)

    def __init__(self, parent=None):
        """Initiate the widget."""
        super(ProjectSettingsForm, self).__init__(parent)
        self._setup_ui()
        self._connect_signals()

    def templates(self):
        """Return list of templates."""
        templates = []

        for index in range(self._tab_widget.count()):
            widget = self._tab_widget.widget(index)
            identifier = self._tab_widget.tabText(index)
            templates.append(widget.template(identifier))

        return tuple(templates)

    def set_values(self, config):
        """Initialize values."""
        self._tab_widget.clear()

        for _config in config.project_template_configs:
            widget = _ProjectTemplateForm()
            widget.set_values(_config)
            widget.updated.connect(self._template_updated)
            self._tab_widget.addTab(widget, _config.id)

    def _setup_ui(self):
        """Initialize user interface."""
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(10, 20, 10, 10)
        main_layout.setSpacing(15)

        self._tab_widget = EditableTabWidget(self)
        self._tab_widget.set_instruction(
            "Add naming convention for Nuke Studio or Hiero projects (.hrox)\n"
            "by clicking the '+' button on the top-right corner."
        )
        main_layout.addWidget(self._tab_widget)

    def _connect_signals(self):
        """Initialize signals connection."""
        self._tab_widget.new_tab_requested.connect(self._add_template)
        self._tab_widget.tab_removed.connect(self._template_updated)
        self._tab_widget.tab_edited.connect(self._template_updated)

    def _add_template(self):
        """Add a new tab for template."""
        identifier = "Project{}".format(self._tab_widget.count() + 1)

        widget = _ProjectTemplateForm()
        widget.updated.connect(self._template_updated)

        self._tab_widget.addTab(widget, identifier)
        self._tab_widget.setCurrentWidget(widget)

        self._template_updated()

    def _template_updated(self):
        """Emit signal once a template has been updated."""
        self.updated.emit("project_template_configs", self.templates())


class _CompTemplateForm(QtWidgets.QWidget):
    """Form to manage comp template settings."""

    #: :term:`Qt Signal` emitted when the template is updated.
    updated = QtCore.Signal()

    def __init__(self, parent=None):
        """Initiate the widget."""
        super(_CompTemplateForm, self).__init__(parent)
        self._setup_ui()
        self._connect_signals()

    def template(self, identifier):
        """Return template object."""
        return TemplateConfig(
            id=identifier,
            pattern_path=self._template_form.pattern_path(),
            pattern_base=self._template_form.pattern_base(),
            default_expression=self._template_form.default_expression(),
            match_start=self._template_form.match_start(),
            match_end=self._template_form.match_end(),
            outputs=self.output_templates()
        )

    def output_templates(self):
        """Return list of output templates."""
        templates = []

        for index in range(self._tab_widget.count()):
            widget = self._tab_widget.widget(index)
            identifier = self._tab_widget.tabText(index)
            templates.append(widget.template(identifier))

        return tuple(templates)

    def set_values(self, config):
        """Initialize values."""
        self._template_form.blockSignals(True)
        self._template_form.set_values(config)
        self._template_form.blockSignals(False)

        self._tab_widget.clear()

        for _config in config.outputs:
            widget = _OutputTemplateForm()
            widget.set_values(_config)
            widget.updated.connect(self.updated.emit)
            self._tab_widget.addTab(widget, _config.id)

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
        self._template_form.updated.connect(self.updated.emit)
        self._tab_widget.new_tab_requested.connect(self._add_output_template)
        self._tab_widget.tab_removed.connect(lambda: self.updated.emit())
        self._tab_widget.tab_edited.connect(lambda: self.updated.emit())

    def _add_output_template(self):
        """Add a new tab for output template."""
        identifier = "Output{}".format(self._tab_widget.count() + 1)

        widget = _OutputTemplateForm()
        widget.updated.connect(self.updated.emit)

        self._tab_widget.addTab(widget, identifier)
        self._tab_widget.setCurrentWidget(widget)

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

    def template(self, identifier):
        """Return template object."""
        return TemplateConfig(
            id=identifier,
            pattern_path=self._template_form.pattern_path(),
            pattern_base=self._template_form.pattern_base(),
            default_expression=self._template_form.default_expression(),
            match_start=self._template_form.match_start(),
            match_end=self._template_form.match_end(),
            outputs=None
        )

    def set_values(self, config):
        """Initialize values."""
        self._template_form.blockSignals(True)
        self._template_form.set_values(config)
        self._template_form.blockSignals(False)

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
        self._template_form.updated.connect(self.updated.emit)


class _OutputTemplateForm(QtWidgets.QWidget):
    """Form to manage output template settings."""

    #: :term:`Qt Signal` emitted when the template is updated.
    updated = QtCore.Signal()

    def __init__(self, parent=None):
        """Initiate the widget."""
        super(_OutputTemplateForm, self).__init__(parent)
        self._setup_ui()
        self._connect_signals()

    def template(self, identifier):
        """Return template object."""
        return TemplateConfig(
            id=identifier,
            pattern_path=self._template_form.pattern_path(),
            pattern_base=self._template_form.pattern_base(),
            default_expression=self._template_form.default_expression(),
            match_start=self._template_form.match_start(),
            match_end=self._template_form.match_end(),
            outputs=None
        )

    def set_values(self, config):
        """Initialize values."""
        self._template_form.blockSignals(True)
        self._template_form.set_values(config)
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
        self._template_form.updated.connect(self.updated.emit)


class _TemplateForm(QtWidgets.QWidget):
    """Form to manage template path and name."""

    #: :term:`Qt Signal` emitted when a key of the template has changed.
    updated = QtCore.Signal()

    def __init__(self, parent=None):
        """Initiate the widget."""
        super(_TemplateForm, self).__init__(parent)
        self._setup_ui()
        self._connect_signals()

        default_config = load_template_configs([{"id": "Default"}])[0]
        self.set_values(default_config)

    def pattern_path(self):
        """Return pattern path."""
        return self._pattern_path.text()

    def pattern_base(self):
        """Return pattern base."""
        return self._pattern_base.text()

    def default_expression(self):
        """Return default expression."""
        return self._default_expression.text()

    def match_start(self):
        """Return whether path should match exactly the start of the pattern."""
        return self._match_start.isChecked()

    def match_end(self):
        """Return whether path should match exactly the end of the pattern."""
        return self._match_end.isChecked()

    def set_values(self, config):
        """Initialize values."""
        self._pattern_path.blockSignals(True)
        self._pattern_path.setText(config.pattern_path)
        self._pattern_path.blockSignals(False)

        self._pattern_base.blockSignals(True)
        self._pattern_base.setText(config.pattern_base)
        self._pattern_base.blockSignals(False)

        self._default_expression.blockSignals(True)
        self._default_expression.setText(config.default_expression)
        self._default_expression.blockSignals(False)

        self._match_start.blockSignals(True)
        state = QtCore.Qt.Checked if config.match_start else QtCore.Qt.Unchecked
        self._match_start.setCheckState(state)
        self._match_start.blockSignals(False)

        self._match_end.blockSignals(True)
        state = QtCore.Qt.Checked if config.match_end else QtCore.Qt.Unchecked
        self._match_end.setCheckState(state)
        self._match_end.blockSignals(False)

    def _setup_ui(self):
        """Initialize user interface."""
        main_layout = QtWidgets.QGridLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(8)

        pattern_path_lbl = QtWidgets.QLabel("Pattern Path", self)
        main_layout.addWidget(pattern_path_lbl, 0, 0, 1, 1)

        self._pattern_path = QtWidgets.QLineEdit(self)
        main_layout.addWidget(self._pattern_path, 0, 1, 1, 1)

        pattern_base_lbl = QtWidgets.QLabel("Pattern Base", self)
        main_layout.addWidget(pattern_base_lbl, 1, 0, 1, 1)

        self._pattern_base = QtWidgets.QLineEdit(self)
        main_layout.addWidget(self._pattern_base, 1, 1, 1, 1)

        default_expression_lbl = QtWidgets.QLabel("Default Expression", self)
        main_layout.addWidget(default_expression_lbl, 2, 0, 1, 1)

        self._default_expression = QtWidgets.QLineEdit(self)
        main_layout.addWidget(self._default_expression, 2, 1, 1, 1)

        self._match_start = QtWidgets.QCheckBox("Match Start Pattern Exactly", self)
        main_layout.addWidget(self._match_start, 3, 1, 1, 1)

        self._match_end = QtWidgets.QCheckBox("Match End Pattern Exactly", self)
        main_layout.addWidget(self._match_end, 4, 1, 1, 1)

    def _connect_signals(self):
        """Initialize signals connection."""
        self._pattern_path.textChanged.connect(lambda: self.updated.emit())
        self._pattern_base.textChanged.connect(lambda: self.updated.emit())
        self._default_expression.textChanged.connect(lambda: self.updated.emit())
        self._match_start.stateChanged.connect(lambda: self.updated.emit())
        self._match_end.stateChanged.connect(lambda: self.updated.emit())


class ColorspaceSettingsForm(QtWidgets.QWidget):
    """Form to manage colorspace settings."""

    #: :term:`Qt Signal` emitted when a key of the config has changed.
    updated = QtCore.Signal(str, object)

    def __init__(self, parent=None):
        """Initiate the widget."""
        super(ColorspaceSettingsForm, self).__init__(parent)
        self._setup_ui()
        self._connect_signals()

    def set_values(self, config):
        """Initialize values."""
        self._colorspace_table.blockSignals(True)
        self._colorspace_table.set_values(config.colorspace_aliases)
        self._colorspace_table.blockSignals(False)

    def _setup_ui(self):
        """Initialize user interface."""
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(10, 20, 10, 10)
        main_layout.setSpacing(8)

        colorspace_lbl = QtWidgets.QLabel("Define aliases for colorspace token value", self)
        main_layout.addWidget(colorspace_lbl)

        self._colorspace_table = EditableTable(["Value", "Alias"], [200], self)
        main_layout.addWidget(self._colorspace_table)

    def _connect_signals(self):
        """Initialize signals connection."""
        self._colorspace_table.updated.connect(
            lambda values: self.updated.emit("colorspace_aliases", values)
        )


class TokenSettingsForm(QtWidgets.QWidget):
    """Form to manage token settings."""

    #: :term:`Qt Signal` emitted when a key of the config has changed.
    updated = QtCore.Signal(str, object)

    def __init__(self, parent=None):
        """Initiate the widget."""
        super(TokenSettingsForm, self).__init__(parent)
        self._setup_ui()
        self._connect_signals()

    def set_values(self, config):
        """Initialize values."""
        self._token_table.blockSignals(True)
        self._token_table.set_values(config.tokens)
        self._token_table.blockSignals(False)

    def _setup_ui(self):
        """Initialize user interface."""
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(10, 20, 10, 10)
        main_layout.setSpacing(8)

        token_lbl = QtWidgets.QLabel("Add tokens to resolve in patterns", self)
        main_layout.addWidget(token_lbl)

        self._token_table = EditableTable(["Key", "Value"], [200], self)
        main_layout.addWidget(self._token_table)

    def _connect_signals(self):
        """Initialize signals connection."""
        self._token_table.updated.connect(
            lambda values: self.updated.emit("tokens", values)
        )


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
