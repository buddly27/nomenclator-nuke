# -*- coding: utf-8 -*-

from nomenclator.vendor.Qt import QtWidgets, QtCore

from .group_widget import GroupWidget
from .output_list import OutputList


class OutputSettingsForm(QtWidgets.QWidget):
    """Form to manage render outputs settings."""

    def __init__(self, parent=None):
        """Initiate the widget."""
        super(OutputSettingsForm, self).__init__(parent)
        self._setup_ui()
        self._connect_signals()

    def set_values(self, context):
        """Initialize values."""
        self._file_path_form.set_values(context)
        self._file_name_form.set_values(context)
        self._output_list.set_values(context.outputs)

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


class FilePathForm(QtWidgets.QWidget):
    """Form to manage output file path settings."""

    def __init__(self, parent=None):
        """Initiate the widget."""
        super(FilePathForm, self).__init__(parent)
        self._setup_ui()

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

        self._destination = QtWidgets.QComboBox(self)
        main_layout.addWidget(self._destination, 0, 1)

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


class FileNameForm(QtWidgets.QWidget):
    """Form to manage output file name settings."""

    def __init__(self, parent=None):
        """Initiate the widget."""
        super(FileNameForm, self).__init__(parent)
        self._setup_ui()

    def set_values(self, context):
        """Initialize values."""
        self._padding.blockSignals(True)
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


def _compute_check_state(values_set):
    """Compute checkbox state from values set."""
    if values_set == {True}:
        return QtCore.Qt.Checked
    elif values_set == {False}:
        return QtCore.Qt.Unchecked

    return QtCore.Qt.PartiallyChecked
