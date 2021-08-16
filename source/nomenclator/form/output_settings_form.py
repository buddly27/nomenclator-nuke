# -*- coding: utf-8 -*-

from nomenclator.vendor.Qt import QtWidgets

from nomenclator.widget import GroupFormWidget
from nomenclator.widget import PathWidget


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

        sub_folder_group = GroupFormWidget(
            self._sub_folder_form,
            vertical_stretch=False, parent=self
        )
        sub_folder_group.setTitle("Append to Sub-Folder")
        main_layout.addWidget(sub_folder_group, 0, 4, 2, 1)

        self._file_name_form = FileNameForm(self)

        file_name_group = GroupFormWidget(
            self._file_name_form,
            vertical_stretch=False, parent=self
        )
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
