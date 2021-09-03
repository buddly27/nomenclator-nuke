# -*- coding: utf-8 -*-

from nomenclator.vendor.Qt import QtWidgets, QtCore

from .group_widget import GroupWidget
from .output_list import OutputList


class OutputSettingsForm(QtWidgets.QWidget):
    """Form to manage render outputs settings."""

    #: :term:`Qt Signal` emitted when input context is updated.
    updated = QtCore.Signal()

    def __init__(self, parent=None):
        """Initiate the widget."""
        super(OutputSettingsForm, self).__init__(parent)
        self._setup_ui()
        self._connect_signals()

        self._context = None

    @property
    def context(self):
        """Return updated context."""
        return self._context

    def set_values(self, context):
        """Initialize values."""
        self._file_path_form.set_values(context)
        self._file_name_form.set_values(context)
        self._output_list.set_values(context.outputs)

        self._context = context

    def update(self, context):
        """Update values from context."""
        self._file_path_form.update(context)
        self._output_list.update(context.outputs)

        self._context = context

    def _setup_ui(self):
        """Initialize user interface."""
        self.setObjectName("output-form")

        main_layout = QtWidgets.QGridLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(8)

        self._file_path_form = FilePathForm(self)
        self._file_path_form.setMinimumHeight(100)

        file_path_group = GroupWidget(self._file_path_form, self)
        file_path_group.setTitle("File Path")
        main_layout.addWidget(file_path_group, 0, 0)

        self._file_name_form = FileNameForm(self)
        self._file_name_form.setMinimumHeight(100)

        file_name_group = GroupWidget(self._file_name_form, self)
        file_name_group.setTitle("File Name")
        main_layout.addWidget(file_name_group, 0, 1)

        self._output_list = OutputList(self)
        main_layout.addWidget(self._output_list, 1, 0, 1, 2)
        main_layout.rowStretch(1)

    def _connect_signals(self):
        """Initialize signals connection."""
        self._output_list.updated.connect(self._handle_output_update)
        self._file_name_form.output_updated.connect(self._handle_global_output_update)
        self._file_path_form.output_updated.connect(self._handle_global_output_update)
        self._file_name_form.updated.connect(self._update_context)
        self._file_path_form.updated.connect(self._update_context)

    def _handle_output_update(self):
        """Handle changes to output list"""
        outputs = self._output_list.outputs_context()
        self._update_context("outputs", outputs)

        self._file_path_form.set_values(self._context)
        self._file_name_form.set_values(self._context)

    def _handle_global_output_update(self, key, value):
        """Handle global changes to options"""
        method_name = "set_{}".format(key)
        setter = getattr(self._output_list, method_name, None)
        setter(value)

        outputs = self._output_list.outputs_context()
        self._update_context("outputs", outputs)

    def _update_context(self, key, value):
        """Update context object from *key* and *value*."""
        # noinspection PyProtectedMember
        self._context = self._context._replace(**{key: value})

        self.updated.emit()


class FilePathForm(QtWidgets.QWidget):
    """Form to manage output file path settings."""

    #: :term:`Qt Signal` emitted when a key of the context has changed.
    updated = QtCore.Signal(str, object)

    #: :term:`Qt Signal` emitted when an global output key of the context has changed.
    output_updated = QtCore.Signal(str, object)

    #: Label to indicate that destinations are set per output.
    DESTINATION_PER_OUTPUT = "-- per output --"

    def __init__(self, parent=None):
        """Initiate the widget."""
        super(FilePathForm, self).__init__(parent)
        self._setup_ui()
        self._connect_signals()

    @property
    def append_passname(self):
        """Return whether passname should be appended to subfolder."""
        return self._append_passname.isChecked()

    def set_values(self, context):
        """Initialize values."""
        self._create_subfolders.blockSignals(True)
        state = QtCore.Qt.Checked if context.create_subfolders else QtCore.Qt.Unchecked
        self._create_subfolders.setCheckState(state)
        self._create_subfolders.blockSignals(False)

        self._append_passname.blockSignals(True)
        state = _compute_check_state({
            output.append_passname_to_subfolder for output in context.outputs
        })
        self._append_passname.setCheckState(state)
        self._append_passname.blockSignals(False)

    def update(self, context):
        """Update values from context."""
        self._destinations.blockSignals(True)
        self._destinations.clear()

        items = []
        if len(context.outputs):
            items = list(context.outputs[0].destinations)

        if len(items):
            items += [self.DESTINATION_PER_OUTPUT]
            self._destinations.addItems(items)

            targets = set([output.destination for output in context.outputs])
            value = list(targets)[0] if len(targets) == 1 else self.DESTINATION_PER_OUTPUT

            index = self._destinations.findText(value)
            if index >= 0:
                self._destinations.setCurrentIndex(index)

        self._destinations.blockSignals(False)

    def _setup_ui(self):
        """Initialize user interface."""
        self.setSizePolicy(
            QtWidgets.QSizePolicy(
                QtWidgets.QSizePolicy.Preferred,
                QtWidgets.QSizePolicy.Minimum
            )
        )

        main_layout = QtWidgets.QGridLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(5)

        label = QtWidgets.QLabel("Destination", self)
        label.setMaximumWidth(80)
        main_layout.addWidget(label, 0, 0)

        self._destinations = QtWidgets.QComboBox(self)
        main_layout.addWidget(self._destinations, 0, 1)

        self._append_passname = QtWidgets.QCheckBox(
            "Append passname to each sub-folder", self
        )
        main_layout.addWidget(self._append_passname, 1, 0, 1, 2)

        self._create_subfolders = QtWidgets.QCheckBox("Create sub-folders now", self)
        main_layout.addWidget(self._create_subfolders, 2, 0, 1, 2)

        spacer = QtWidgets.QSpacerItem(
            0, 0, QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Expanding
        )
        main_layout.addItem(spacer, 3, 0, 1, 2)

    def _connect_signals(self):
        """Initialize signals connection."""
        self._append_passname.stateChanged.connect(self._emit_output_signal)
        self._destinations.currentIndexChanged.connect(self._emit_output_signal)

        self._create_subfolders.stateChanged.connect(
            lambda state: self.updated.emit(
                "create_subfolders", state == QtCore.Qt.Checked
            )
        )

    def _emit_output_signal(self):
        """Emit signal to indicate that output items must be updated."""
        knob = self.sender()

        context_attributes = {
            self._append_passname: "append_passname_to_subfolder",
            self._destinations: "destination",
        }

        # Fetch value depending on the knob type.
        if isinstance(knob, QtWidgets.QCheckBox):
            value = knob.isChecked()
        else:
            value = knob.currentText()

        # Ignore if value is a placeholder for multi destinations.
        if value == self.DESTINATION_PER_OUTPUT:
            return

        self.output_updated.emit(context_attributes[knob], value)

        if not isinstance(knob, QtWidgets.QCheckBox):
            return

        # Ensure that the checkbox is not partially checked if user click on it.
        if knob.checkState() == QtCore.Qt.PartiallyChecked:
            knob.blockSignals(True)
            knob.setCheckState(QtCore.Qt.Checked)
            knob.blockSignals(False)


class FileNameForm(QtWidgets.QWidget):
    """Form to manage output file name settings."""

    #: :term:`Qt Signal` emitted when a key of the context has changed.
    updated = QtCore.Signal(str, object)

    #: :term:`Qt Signal` emitted when an global output key of the context has changed.
    output_updated = QtCore.Signal(str, object)

    def __init__(self, parent=None):
        """Initiate the widget."""
        super(FileNameForm, self).__init__(parent)
        self._setup_ui()
        self._connect_signals()

    @property
    def append_passname(self):
        """Return whether passname should be appended to subfolder."""
        return self._append_passname.isChecked()

    @property
    def append_colorspace(self):
        """Return whether colorspace should be appended to subfolder."""
        return self._append_colorspace.isChecked()

    @property
    def append_username(self):
        """Return whether username should be appended to subfolder."""
        return self._append_username.isChecked()

    def set_values(self, context):
        """Initialize values."""
        self._padding.blockSignals(True)
        self._padding.clear()
        self._padding.addItems(context.paddings)
        index = self._padding.findText(context.padding)
        if index >= 0:
            self._padding.setCurrentIndex(index)
        self._padding.blockSignals(False)

        self._append_passname.blockSignals(True)
        state = _compute_check_state({
            output.append_passname_to_name for output in context.outputs
        })
        self._append_passname.setCheckState(state)
        self._append_passname.blockSignals(False)

        self._append_colorspace.blockSignals(True)
        state = _compute_check_state({
            output.append_colorspace_to_name for output in context.outputs
        })
        self._append_colorspace.setCheckState(state)
        self._append_colorspace.blockSignals(False)

        self._append_username.blockSignals(True)
        state = _compute_check_state({
            output.append_username_to_name for output in context.outputs
        })
        self._append_username.setCheckState(state)
        self._append_username.blockSignals(False)

    def _setup_ui(self):
        """Initialize user interface."""
        main_layout = QtWidgets.QGridLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(5)

        label = QtWidgets.QLabel("Padding", self)
        label.setMaximumWidth(80)
        main_layout.addWidget(label, 0, 0)

        self._padding = QtWidgets.QComboBox(self)
        main_layout.addWidget(self._padding, 0, 1)

        self._append_passname = QtWidgets.QCheckBox(
            "Append passname to each output", self
        )
        main_layout.addWidget(self._append_passname, 1, 0, 1, 2)

        self._append_colorspace = QtWidgets.QCheckBox(
            "Append colorspace to each output", self
        )
        main_layout.addWidget(self._append_colorspace, 2, 0, 1, 2)

        self._append_username = QtWidgets.QCheckBox(
            "Append username to each output", self
        )
        main_layout.addWidget(self._append_username, 3, 0, 1, 2)

    def _connect_signals(self):
        """Initialize signals connection."""
        self._append_passname.stateChanged.connect(self._emit_output_signal)
        self._append_username.stateChanged.connect(self._emit_output_signal)
        self._append_colorspace.stateChanged.connect(self._emit_output_signal)

        self._padding.currentTextChanged.connect(
            lambda value: self.updated.emit("padding", value)
        )

    def _emit_output_signal(self):
        """Emit corresponding signals"""
        knob = self.sender()
        context_attributes = {
            self._append_passname: "append_passname_to_name",
            self._append_username: "append_username_to_name",
            self._append_colorspace: "append_colorspace_to_name",
        }

        self.output_updated.emit(context_attributes[knob], knob.isChecked())

        # Ensure that the checkbox is not partially checked if user click on it.
        if knob.checkState() == QtCore.Qt.PartiallyChecked:
            knob.blockSignals(True)
            knob.setCheckState(QtCore.Qt.Checked)
            knob.blockSignals(False)


def _compute_check_state(values_set):
    """Compute checkbox state from values set."""
    if values_set == {True}:
        return QtCore.Qt.Checked
    elif values_set == {False}:
        return QtCore.Qt.Unchecked

    return QtCore.Qt.PartiallyChecked
