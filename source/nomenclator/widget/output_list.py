# -*- coding: utf-8 -*-

from nomenclator.vendor.Qt import QtWidgets, QtCore

import nomenclator.context

from .group_widget import GroupWidget
from .path_widget import PathWidget


class OutputList(QtWidgets.QListWidget):
    """List of output form settings."""

    #: :term:`Qt Signal` emitted when outputs are updated.
    updated = QtCore.Signal()

    def __init__(self, parent=None):
        """Initiate the widget."""
        super(OutputList, self).__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        """Initialize user interface."""
        self.setObjectName("output-list")
        self.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)

    def outputs_context(self):
        """Return list of output contexts."""
        outputs = []

        for index in range(self.count()):
            item = self.item(index)
            widget = self.itemWidget(item)

            context = nomenclator.context.OutputContext(
                name=widget.form.name,
                blacklisted_names=widget.form.blacklisted_names,
                path=widget.form.path,
                passname=widget.form.name,
                enabled=widget.is_enabled(),
                destination=widget.form.destination,
                destinations=widget.form.destinations,
                file_type=widget.form.file_type,
                file_types=widget.form.file_types,
                append_username_to_name=widget.form.append_username_to_name,
                append_colorspace_to_name=widget.form.append_colorspace_to_name,
                append_passname_to_name=widget.form.append_passname_to_name,
                append_passname_to_subfolder=widget.form.append_passname_to_subfolder
            )

            outputs.append(context)

        return tuple(outputs)

    def set_values(self, outputs_context):
        """Initialize values."""
        self.clear()

        for context in outputs_context:
            form = SettingsForm(context, self)
            widget = SelectableItemWidget(form, context.enabled, self)

            form.updated.connect(self.updated)
            widget.updated.connect(self.updated)

            item = QtWidgets.QListWidgetItem()
            item.setSizeHint(widget.sizeHint())
            self.addItem(item)
            self.setItemWidget(item, widget)

    def set_append_username_to_name(self, value):
        """Indicate whether username should be appended to all base name."""
        for index in range(self.count()):
            item = self.item(index)
            widget = self.itemWidget(item)

            widget.form.set_append_username_to_name(value)

    def set_append_colorspace_to_name(self, value):
        """Indicate whether colorspace should be appended to all base name."""
        for index in range(self.count()):
            item = self.item(index)
            widget = self.itemWidget(item)

            widget.form.set_append_colorspace_to_name(value)

    def set_append_passname_to_name(self, value):
        """Indicate whether passname should be appended to all base name."""
        for index in range(self.count()):
            item = self.item(index)
            widget = self.itemWidget(item)

            widget.form.set_append_passname_to_name(value)

    def set_append_passname_to_subfolder(self, value):
        """Indicate whether passname should be appended to all subfolder."""
        for index in range(self.count()):
            item = self.item(index)
            widget = self.itemWidget(item)

            widget.form.set_append_passname_to_subfolder(value)


class SelectableItemWidget(QtWidgets.QWidget):
    """Selectable widget embedding another widget within a list"""

    #: :term:`Qt Signal` emitted when the output is updated.
    updated = QtCore.Signal()

    def __init__(self, form_widget, enabled, parent=None):
        """Initiate the widget."""
        super(SelectableItemWidget, self).__init__(parent)
        self._form_widget = form_widget

        self._setup_ui()
        self._connect_signals()

        # Initiate state
        self._selection.setCheckState(
            QtCore.Qt.Checked if enabled else QtCore.Qt.Unchecked
        )
        self._toggle_enable()

    @property
    def form(self):
        """Return embedded form widget."""
        return self._form_widget

    def is_enabled(self):
        """Return whether item is enabled."""
        return self._selection.isChecked()

    def _setup_ui(self):
        """Initialize user interface."""

        main_layout = QtWidgets.QHBoxLayout(self)
        main_layout.setContentsMargins(8, 8, 8, 0)
        main_layout.setSpacing(0)

        self._selection_frame = QtWidgets.QFrame(self)
        self._selection_frame.setObjectName("list-item-selection")
        selection_frame_layout = QtWidgets.QVBoxLayout(self._selection_frame)
        selection_frame_layout.setContentsMargins(5, 5, 5, 5)

        self._selection = QtWidgets.QCheckBox(self._selection_frame)
        selection_frame_layout.addWidget(self._selection)

        main_layout.addWidget(self._selection_frame)

        self._main_frame = QtWidgets.QFrame(self)
        self._main_frame.setObjectName("list-item-form")
        main_frame_layout = QtWidgets.QVBoxLayout(self._main_frame)
        main_frame_layout.setContentsMargins(5, 5, 5, 5)

        self._form_widget.setParent(self._main_frame)
        main_frame_layout.addWidget(self._form_widget)

        main_layout.addWidget(self._main_frame)

    def _connect_signals(self):
        """Initialize signals connection."""
        self._selection.stateChanged.connect(self._toggle_enable)

    def _toggle_enable(self):
        """Toggle the enabling state of the output widget."""
        self._main_frame.setEnabled(self._selection.isChecked())
        self.updated.emit()


class SettingsForm(QtWidgets.QWidget):
    """Form to manage render outputs settings."""

    #: :term:`Qt Signal` emitted when the output is updated.
    updated = QtCore.Signal()

    def __init__(self, context, parent=None):
        """Initiate the widget."""
        super(SettingsForm, self).__init__(parent)
        self._setup_ui()
        self._connect_signals()

        self._blacklisted_names = context.blacklisted_names

        self.set_values(context)

    @property
    def name(self):
        """Return output name."""
        return self._node_name.text()

    @property
    def path(self):
        """Return output path."""
        return self._output_path.path()

    @property
    def blacklisted_names(self):
        """Return blacklisted name."""
        return self._blacklisted_names

    @property
    def passname(self):
        """Return output passname."""
        return self._passname.text()

    @property
    def destination(self):
        """Return output destination selected."""
        return self._destination.currentText()

    @property
    def destinations(self):
        """Return output destinations."""
        return [
            self._destination.itemText(index)
            for index in range(self._destination.count())
        ]

    @property
    def file_type(self):
        """Return output file type selected."""
        return self._file_type.currentText()

    @property
    def file_types(self):
        """Return output file types."""
        return [
            self._file_type.itemText(index)
            for index in range(self._file_type.count())
        ]

    @property
    def append_username_to_name(self):
        """Return whether username should be appended to base name."""
        return self._file_name_form.append_username

    @property
    def append_colorspace_to_name(self):
        """Return whether colorspace should be appended to base name."""
        return self._file_name_form.append_colorspace

    @property
    def append_passname_to_name(self):
        """Return whether passname should be appended to base name."""
        return self._file_name_form.append_passname

    @property
    def append_passname_to_subfolder(self):
        """Return whether passname should be appended to subfolder."""
        return self._sub_folder_form.append_passname

    def set_append_username_to_name(self, value):
        """Indicate whether username should be appended to all base name."""
        self._file_name_form.set_append_username(value)

    def set_append_colorspace_to_name(self, value):
        """Indicate whether colorspace should be appended to all base name."""
        self._file_name_form.set_append_colorspace(value)

    def set_append_passname_to_name(self, value):
        """Indicate whether passname should be appended to all base name."""
        self._file_name_form.set_append_passname(value)

    def set_append_passname_to_subfolder(self, value):
        """Indicate whether passname should be appended to all subfolder."""
        self._sub_folder_form.set_append_passname(value)

    def set_values(self, context):
        """Initialize values."""
        self._node_name.blockSignals(True)
        self._node_name.setText(context.name)
        self._node_name.blockSignals(False)

        self._passname.blockSignals(True)
        self._passname.setText(context.passname)
        self._passname.blockSignals(False)

        self._destination.blockSignals(True)
        self._destination.clear()
        self._destination.addItems([t[0] for t in context.destinations])
        self._destination.blockSignals(False)

        self._file_type.blockSignals(True)
        self._file_type.clear()
        self._file_type.addItems(context.file_types)
        index = self._file_type.findText(context.file_type)
        if index >= 0:
            self._file_type.setCurrentIndex(index)
        self._file_type.blockSignals(False)

        self._sub_folder_form.set_values(context)
        self._file_name_form.set_values(context)

        self._output_path.blockSignals(True)
        self._output_path.set_path(context.path)
        self._output_path.blockSignals(False)

    def _setup_ui(self):
        """Initialize user interface."""
        main_layout = QtWidgets.QGridLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(5)

        node_name_label = QtWidgets.QLabel("Node name", self)
        node_name_label.setMaximumWidth(80)
        main_layout.addWidget(node_name_label, 0, 0, 1, 1)

        self._node_name = QtWidgets.QLineEdit(self)
        main_layout.addWidget(self._node_name, 0, 1, 1, 1)

        passname_label = QtWidgets.QLabel("Passname", self)
        passname_label.setMaximumWidth(60)
        main_layout.addWidget(passname_label, 0, 2, 1, 1)

        self._passname = QtWidgets.QLineEdit(self)
        main_layout.addWidget(self._passname, 0, 3, 1, 1)

        destination_label = QtWidgets.QLabel("Destination", self)
        destination_label.setMaximumWidth(80)
        main_layout.addWidget(destination_label, 1, 0, 1, 1)

        self._destination = QtWidgets.QComboBox(self)
        main_layout.addWidget(self._destination, 1, 1, 1, 1)

        file_type_label = QtWidgets.QLabel("File Type", self)
        file_type_label.setMaximumWidth(60)
        main_layout.addWidget(file_type_label, 1, 2, 1, 1)

        self._file_type = QtWidgets.QComboBox(self)
        main_layout.addWidget(self._file_type, 1, 3, 1, 1)

        self._sub_folder_form = SubFolderForm(self)
        self._sub_folder_form.setMinimumWidth(150)

        sub_folder_group = GroupWidget(self._sub_folder_form, self)
        sub_folder_group.setTitle("Append to Sub-Folder")
        main_layout.addWidget(sub_folder_group, 0, 4, 2, 1)

        self._file_name_form = FileNameForm(self)

        file_name_group = GroupWidget(self._file_name_form, self)
        file_name_group.setTitle("Append to File Name")
        main_layout.addWidget(file_name_group, 0, 5, 2, 1)

        self._output_path = PathWidget(self)
        main_layout.addWidget(self._output_path, 2, 0, 1, 6)

    def _connect_signals(self):
        """Initialize signals connection."""
        self._node_name.textChanged.connect(lambda: self.updated.emit())
        self._passname.textChanged.connect(lambda: self.updated.emit())
        self._destination.currentIndexChanged.connect(lambda: self.updated.emit())
        self._file_type.currentIndexChanged.connect(lambda: self.updated.emit())
        self._sub_folder_form.updated.connect(lambda: self.updated.emit())
        self._file_name_form.updated.connect(lambda: self.updated.emit())


class SubFolderForm(QtWidgets.QWidget):
    """Form to manage sub-folder settings."""

    #: :term:`Qt Signal` emitted when the output is updated.
    updated = QtCore.Signal()

    def __init__(self, parent=None):
        """Initiate the widget."""
        super(SubFolderForm, self).__init__(parent)
        self._setup_ui()
        self._connect_signals()

    @property
    def append_passname(self):
        """Return whether passname should be appended to subfolder."""
        return self._append_passname.isChecked()

    def set_append_passname(self, value):
        """Indicate whether passname should be appended to base name."""
        self._append_passname.blockSignals(True)
        state = QtCore.Qt.Checked if value else QtCore.Qt.Unchecked
        self._append_passname.setCheckState(state)
        self._append_passname.blockSignals(False)

    def set_values(self, context):
        """Initialize values."""
        self._append_passname.blockSignals(True)
        state = (
            QtCore.Qt.Checked if context.append_passname_to_subfolder
            else QtCore.Qt.Unchecked
        )
        self._append_passname.setCheckState(state)
        self._append_passname.blockSignals(False)

    def _setup_ui(self):
        """Initialize user interface."""
        main_layout = QtWidgets.QGridLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(5)

        self._append_passname = QtWidgets.QCheckBox("passname", self)
        main_layout.addWidget(self._append_passname, 0, 0)

    def _connect_signals(self):
        """Initialize signals connection."""
        self._append_passname.stateChanged.connect(lambda: self.updated.emit())


class FileNameForm(QtWidgets.QWidget):
    """Form to manage output file name settings."""

    #: :term:`Qt Signal` emitted when the output is updated.
    updated = QtCore.Signal()

    def __init__(self, parent=None):
        """Initiate the widget."""
        super(FileNameForm, self).__init__(parent)
        self._setup_ui()
        self._connect_signals()

    @property
    def append_passname(self):
        """Return whether passname should be appended to base name."""
        return self._append_passname.isChecked()

    @property
    def append_colorspace(self):
        """Return whether colorspace should be appended to base name."""
        return self._append_colorspace.isChecked()

    @property
    def append_username(self):
        """Return whether username should be appended to base name."""
        return self._append_username.isChecked()

    def set_append_username(self, value):
        """Indicate whether username should be appended to base name."""
        self._append_username.blockSignals(True)
        state = QtCore.Qt.Checked if value else QtCore.Qt.Unchecked
        self._append_username.setCheckState(state)
        self._append_username.blockSignals(False)

    def set_append_colorspace(self, value):
        """Indicate whether colorspace should be appended to base name."""
        self._append_colorspace.blockSignals(True)
        state = QtCore.Qt.Checked if value else QtCore.Qt.Unchecked
        self._append_colorspace.setCheckState(state)
        self._append_colorspace.blockSignals(False)

    def set_append_passname(self, value):
        """Indicate whether passname should be appended to base name."""
        self._append_passname.blockSignals(True)
        state = QtCore.Qt.Checked if value else QtCore.Qt.Unchecked
        self._append_passname.setCheckState(state)
        self._append_passname.blockSignals(False)

    def set_values(self, context):
        """Initialize values."""
        self._append_passname.blockSignals(True)
        state = (
            QtCore.Qt.Checked if context.append_passname_to_name
            else QtCore.Qt.Unchecked
        )
        self._append_passname.setCheckState(state)
        self._append_passname.blockSignals(False)

        self._append_colorspace.blockSignals(True)
        state = (
            QtCore.Qt.Checked if context.append_colorspace_to_name
            else QtCore.Qt.Unchecked
        )
        self._append_colorspace.setCheckState(state)
        self._append_colorspace.blockSignals(False)

        self._append_username.blockSignals(True)
        state = (
            QtCore.Qt.Checked if context.append_username_to_name
            else QtCore.Qt.Unchecked
        )
        self._append_username.setCheckState(state)
        self._append_username.blockSignals(False)

    def _setup_ui(self):
        """Initialize user interface."""
        main_layout = QtWidgets.QGridLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(5)

        self._append_passname = QtWidgets.QCheckBox("passname", self)
        main_layout.addWidget(self._append_passname, 0, 0)

        self._append_colorspace = QtWidgets.QCheckBox("colorspace", self)
        main_layout.addWidget(self._append_colorspace, 0, 1)

        self._append_username = QtWidgets.QCheckBox("username", self)
        main_layout.addWidget(self._append_username, 0, 2)

    def _connect_signals(self):
        """Initialize signals connection."""
        self._append_passname.stateChanged.connect(lambda: self.updated.emit())
        self._append_colorspace.stateChanged.connect(lambda: self.updated.emit())
        self._append_username.stateChanged.connect(lambda: self.updated.emit())
