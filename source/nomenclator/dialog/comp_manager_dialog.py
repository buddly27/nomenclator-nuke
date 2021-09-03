# -*- coding: utf-8 -*-

from nomenclator.vendor.Qt import QtWidgets, QtCore
from nomenclator.widget import LocationWidget
from nomenclator.widget import GroupWidget
from nomenclator.widget import DescriptionSelector
from nomenclator.widget import PathWidget
from nomenclator.widget import VersionWidget
from nomenclator.widget import OutputSettingsForm
import nomenclator.utilities

from .theme import classic_style


class CompoManagerDialog(QtWidgets.QDialog):

    def __init__(self, context, parent=None):
        """Initiate dialog."""
        super(CompoManagerDialog, self).__init__(parent)
        self._setup_ui()
        self._connect_signals()

        self._initial_context = context
        self._context = context

        self.set_values(context)
        self._location.setFocus()

    def set_values(self, context):
        """Initialize values."""
        self._location.blockSignals(True)
        self._location.set_items(
            context.recent_locations,
            context.path
        )
        self._location.blockSignals(False)

        self._comp_settings_form.set_values(context)
        self._outputs_settings_group.setEnabled(len(context.outputs) > 0)
        self._output_settings_form.set_values(context)

    def _setup_ui(self):
        """Initialize user interface."""
        self.setWindowTitle("Nomenclator - Composition Manager")
        self.setMinimumWidth(1100)

        self.setStyleSheet(classic_style())

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self._location = LocationWidget(self)
        main_layout.addWidget(self._location)

        body_layout = QtWidgets.QVBoxLayout()
        body_layout.setContentsMargins(10, 10, 10, 10)
        body_layout.setSpacing(8)

        self._comp_settings_form = CompSettingsForm(self)

        comp_settings_group = GroupWidget(self._comp_settings_form, self)
        comp_settings_group.setTitle("Composition")
        body_layout.addWidget(comp_settings_group)

        self._output_settings_form = OutputSettingsForm(self)

        self._outputs_settings_group = GroupWidget(self._output_settings_form, self)
        self._outputs_settings_group.set_vertical_stretch(True)
        self._outputs_settings_group.setTitle("Render Outputs")
        body_layout.addWidget(self._outputs_settings_group)

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
        self._output_settings_form.updated.connect(self._update_full_context)
        self._comp_settings_form.updated.connect(self._update_context)
        self._location.updated.connect(
            lambda: self._update_context("location_path", self._location.value)
        )

    def _update_full_context(self):
        """Replace context object."""
        self._context = self._output_settings_form.context
        self._update_buttons_states()

    def _update_context(self, key, value):
        """Update context object from *key* and *value*."""
        # noinspection PyProtectedMember
        self._context = self._context._replace(**{key: value})
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
            self._context = self._initial_context
            self.set_values(self._context)
            self._update_buttons_states()

    def _update_buttons_states(self):
        """Modify the state of the buttons depending on the config state."""
        button = self._button_box.button(QtWidgets.QDialogButtonBox.Reset)
        button.setEnabled(self._context != self._initial_context)

        button = self._button_box.button(QtWidgets.QDialogButtonBox.Apply)
        button.setEnabled(
            len(self._context.path)
            and all(
                output_context.enabled and len(output_context.path)
                for output_context in self._context.outputs
            )
        )


class CompSettingsForm(QtWidgets.QWidget):
    """Form to manage composition settings."""

    #: :term:`Qt Signal` emitted when a key of the context has changed.
    updated = QtCore.Signal(str, object)

    def __init__(self, parent=None):
        """Initiate the widget."""
        super(CompSettingsForm, self).__init__(parent)
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

        self._version_widget.set_value(context.version)

    def _setup_ui(self):
        """Initialize user interface."""
        main_layout = QtWidgets.QGridLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(8)

        self._description_selector = DescriptionSelector(self)
        main_layout.addWidget(self._description_selector, 0, 0)

        self._append_username = QtWidgets.QCheckBox("Append username to script", self)
        main_layout.addWidget(self._append_username, 1, 0)

        self._script_path = PathWidget(self)
        main_layout.addWidget(self._script_path, 2, 0, 1, 2)

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
