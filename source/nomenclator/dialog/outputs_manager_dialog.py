# -*- coding: utf-8 -*-


from nomenclator.vendor.Qt import QtWidgets, QtCore
from nomenclator.widget import ErrorManagerWidget
from nomenclator.widget import OutputSettingsForm
import nomenclator.context

from .theme import classic_style


class OutputsManagerDialog(QtWidgets.QDialog):

    def __init__(self, context, parent=None):
        """Initiate dialog."""
        super(OutputsManagerDialog, self).__init__(parent)
        self._setup_ui()
        self._connect_signals()

        context = nomenclator.context.update(
            context, discover_next_version=False
        )
        self._initial_context = context
        self._context = context

        self.set_values(context)
        self.update(context)

    @property
    def context(self):
        """Return updated context."""
        return self._context

    def set_values(self, context):
        """Initialize values."""
        self._output_settings_form.set_values(context)

    def update(self, context):
        """Update values from context."""
        self._error_manager_widget.set_values(context)
        self._output_settings_form.update(context)

        self._update_buttons_states()

    def _setup_ui(self):
        """Initialize user interface."""
        self.setWindowTitle("Nomenclator - Outputs Manager")
        self.resize(QtCore.QSize(1100, 600))

        self.setStyleSheet(classic_style())

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self._error_manager_widget = ErrorManagerWidget(self)
        main_layout.addWidget(self._error_manager_widget)

        body_layout = QtWidgets.QVBoxLayout()
        body_layout.setContentsMargins(10, 10, 10, 10)
        body_layout.setSpacing(8)

        self._output_settings_form = OutputSettingsForm(self)
        body_layout.addWidget(self._output_settings_form)

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

    def _update_full_context(self):
        """Replace context object."""
        self._context = self._output_settings_form.context

        # Check if names can be generated.
        self._context = nomenclator.context.update(
            self._context, discover_next_version=False
        )
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
        button.setEnabled(
            all(
                len(output_context.path)
                for output_context in self._context.outputs
            )
        )
