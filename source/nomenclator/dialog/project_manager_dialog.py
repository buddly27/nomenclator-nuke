# -*- coding: utf-8 -*-

import os

from nomenclator.vendor.Qt import QtWidgets, QtCore
from nomenclator.widget import LocationWidget
from nomenclator.widget import ErrorManagerWidget
from nomenclator.widget import GroupWidget
from nomenclator.widget import DescriptionSelector
from nomenclator.widget import PathWidget
from nomenclator.widget import VersionWidget
import nomenclator.context

from .theme import classic_style


class ProjectManagerDialog(QtWidgets.QDialog):

    def __init__(self, context, parent=None):
        """Initiate dialog."""
        super(ProjectManagerDialog, self).__init__(parent)
        self._setup_ui()
        self._connect_signals()

        context = nomenclator.context.update(context)
        self._initial_context = context
        self._context = context

        self.set_values(context)
        self.update(context)

        self._location.setFocus()

    @property
    def context(self):
        """Return updated context."""
        return self._context

    def set_values(self, context):
        """Initialize values."""
        self._location.blockSignals(True)
        self._location.set_items(
            context.recent_locations,
            os.path.dirname(context.path)
        )
        self._location.blockSignals(False)

        self._project_settings_form.set_values(context)

    def update(self, context):
        """Update values from context."""
        self._error_manager_widget.set_values(context)
        self._project_settings_form.update(context)

        self._update_buttons_states()

    def _setup_ui(self):
        """Initialize user interface."""
        self.setWindowTitle("Nomenclator - Project Manager")
        self.resize(QtCore.QSize(600, 200))

        self.setStyleSheet(classic_style())

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self._location = LocationWidget(self)
        main_layout.addWidget(self._location)

        self._error_manager_widget = ErrorManagerWidget(self)
        main_layout.addWidget(self._error_manager_widget)

        body_layout = QtWidgets.QVBoxLayout()
        body_layout.setContentsMargins(10, 10, 10, 10)
        body_layout.setSpacing(8)

        self._project_settings_form = ProjectSettingsForm(self)

        comp_settings_group = GroupWidget(self._project_settings_form, self)
        comp_settings_group.setTitle("Project")
        body_layout.addWidget(comp_settings_group)

        spacer = QtWidgets.QSpacerItem(
            0, 0, QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Expanding
        )
        body_layout.addItem(spacer)

        self._button_box = QtWidgets.QDialogButtonBox(self)
        self._button_box.setOrientation(QtCore.Qt.Horizontal)
        self._button_box.addButton(QtWidgets.QDialogButtonBox.Reset)
        self._button_box.addButton(QtWidgets.QDialogButtonBox.Apply)
        self._button_box.addButton(QtWidgets.QDialogButtonBox.Cancel)
        body_layout.addWidget(self._button_box)

        button = self._button_box.button(QtWidgets.QDialogButtonBox.Reset)
        button.setEnabled(False)

        button = self._button_box.button(QtWidgets.QDialogButtonBox.Apply)
        button.setEnabled(False)

        main_layout.addItem(body_layout)

    def _connect_signals(self):
        """Initialize signals connection."""
        self._button_box.clicked.connect(self._button_clicked)
        self._project_settings_form.updated.connect(self._update_context)
        self._location.updated.connect(self._update_location)

    def _update_location(self):
        """Update location path in context."""
        path = self._location.value

        # Ignore last separator if necessary.
        if len(path) > 1 and path.endswith(os.sep):
            path = path[:-1]

        self._update_context("location_path", path)

    def _update_context(self, key, value):
        """Update context object from *key* and *value*."""
        # noinspection PyProtectedMember
        self._context = self._context._replace(**{key: value})

        # Check if names can be generated.
        self._context = nomenclator.context.update(self._context)
        self.update(self._context)

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
            self._context = self._initial_context
            self.set_values(self._context)
            self.update(self._context)

    def _update_buttons_states(self):
        """Modify the state of the buttons depending on the config state."""
        button = self._button_box.button(QtWidgets.QDialogButtonBox.Reset)
        button.setEnabled(self._context != self._initial_context)

        button = self._button_box.button(QtWidgets.QDialogButtonBox.Apply)
        button.setEnabled(len(self._context.path))


class ProjectSettingsForm(QtWidgets.QWidget):
    """Form to manage project settings."""

    #: :term:`Qt Signal` emitted when a key of the context has changed.
    updated = QtCore.Signal(str, object)

    def __init__(self, parent=None):
        """Initiate the widget."""
        super(ProjectSettingsForm, self).__init__(parent)
        self._setup_ui()
        self._connect_signals()

    def set_values(self, context):
        """Initialize values."""
        self._description_selector.blockSignals(True)
        self._description_selector.set_items(context.descriptions)
        self._description_selector.set_current(context.description)
        self._description_selector.blockSignals(False)

        self._append_username.blockSignals(True)
        state = QtCore.Qt.Checked if context.append_username_to_name else QtCore.Qt.Unchecked
        self._append_username.setCheckState(state)
        self._append_username.blockSignals(False)

    def update(self, context):
        """Update values from context."""
        self._project_path.set_path(context.path)
        self._version_widget.set_value(context.version)

    def _setup_ui(self):
        """Initialize user interface."""
        main_layout = QtWidgets.QGridLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(8)

        self._description_selector = DescriptionSelector(self)
        main_layout.addWidget(self._description_selector, 0, 0)

        self._append_username = QtWidgets.QCheckBox("Append username to project", self)
        main_layout.addWidget(self._append_username, 1, 0)

        self._project_path = PathWidget(self)
        main_layout.addWidget(self._project_path, 2, 0, 1, 2)

        self._version_widget = VersionWidget(self)
        main_layout.addWidget(self._version_widget, 0, 1, 2, 1)

    def _connect_signals(self):
        """Initialize signals connection."""
        self._description_selector.updated.connect(
            lambda: self.updated.emit(
                "description", self._description_selector.value()
            )
        )

        self._append_username.stateChanged.connect(
            lambda state: self.updated.emit(
                "append_username_to_name", state == QtCore.Qt.Checked
            )
        )
