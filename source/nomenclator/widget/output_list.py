# -*- coding: utf-8 -*-

from nomenclator.vendor.Qt import QtWidgets, QtCore

from .group_widget import GroupWidget
from .path_widget import PathWidget


class OutputList(QtWidgets.QListWidget):
    """List of output form settings."""

    def __init__(self, parent=None):
        """Initiate the widget."""
        super(OutputList, self).__init__(parent)
        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self):
        """Initialize user interface."""
        self.setObjectName("output-list")
        self.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)

    def _connect_signals(self):
        """Initialize signals connection."""

    def add(self, node, config):
        """Add output item to list."""
        output_form = OutputSettingsForm(node, config, self)
        output_widget = SelectableItemWidget(
            output_form, not node["disable"].value(), self
        )

        item = QtWidgets.QListWidgetItem()
        item.setSizeHint(output_widget.sizeHint())
        self.addItem(item)
        self.setItemWidget(item, output_widget)


class SelectableItemWidget(QtWidgets.QWidget):
    """Selectable widget embedding another widget within a list"""

    def __init__(self, form_widget, enabled, parent=None):
        """Initiate the widget."""
        super(SelectableItemWidget, self).__init__(parent)
        self._setup_ui(form_widget)
        self._connect_signals()

        # Initiate state
        self._selection.setCheckState(
            QtCore.Qt.Checked if enabled else QtCore.Qt.Unchecked
        )
        self._toggle_enable()

    def _setup_ui(self, form_widget):
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

        form_widget.setParent(self._main_frame)
        main_frame_layout.addWidget(form_widget)

        main_layout.addWidget(self._main_frame)

    def _connect_signals(self):
        """Initialize signals connection."""
        self._selection.stateChanged.connect(self._toggle_enable)

    def _toggle_enable(self):
        """Toggle the enabling state of the output widget."""
        self._main_frame.setEnabled(self._selection.isChecked())


class OutputSettingsForm(QtWidgets.QWidget):
    """Form to manage render outputs settings."""

    def __init__(self, node, config, parent=None):
        """Initiate the widget."""
        super(OutputSettingsForm, self).__init__(parent)
        self._setup_ui()

        self._node = node
        self._config = config

        self._initiate()

    def _initiate(self):
        """Initiate values."""
        self._node_name.setText(self._node.name())
        self._passname.setText(self._node.name())
        self._output_path.set_path(self._node["file"].value())

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
        sub_folder_group.expand_vertically(False)
        sub_folder_group.setTitle("Append to Sub-Folder")
        main_layout.addWidget(sub_folder_group, 0, 4, 2, 1)

        self._file_name_form = FileNameForm(self)

        file_name_group = GroupWidget(self._file_name_form, self)
        sub_folder_group.expand_vertically(False)
        file_name_group.setTitle("Append to File Name")
        main_layout.addWidget(file_name_group, 0, 5, 2, 1)

        self._output_path = PathWidget(self)
        main_layout.addWidget(self._output_path, 2, 0, 1, 6)


class SubFolderForm(QtWidgets.QWidget):
    """Form to manage sub-folder settings."""

    def __init__(self, parent=None):
        """Initiate the widget."""
        super(SubFolderForm, self).__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        """Initialize user interface."""
        main_layout = QtWidgets.QGridLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(5)

        self._append_passname = QtWidgets.QCheckBox("passname", self)
        main_layout.addWidget(self._append_passname, 0, 0)


class FileNameForm(QtWidgets.QWidget):
    """Form to manage output file name settings."""

    def __init__(self, parent=None):
        """Initiate the widget."""
        super(FileNameForm, self).__init__(parent)
        self._setup_ui()

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
