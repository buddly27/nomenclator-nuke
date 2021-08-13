# -*- coding: utf-8 -*-

from nomenclator.vendor.Qt import QtWidgets

from nomenclator.widget import GroupFormWidget
from nomenclator.widget import ListFormItemWidget

from .output_settings_form import OutputSettingsForm


class OutputsSettingsForm(QtWidgets.QWidget):
    """Form to manage render outputs settings."""

    def __init__(self, nodes, blacklisted_names, parent=None):
        """Initiate the widget."""
        super(OutputsSettingsForm, self).__init__(parent)
        self._setup_ui(nodes, blacklisted_names)
        self._connect_signals()

    def _setup_ui(self, nodes, blacklisted_names):
        """Initialize user interface."""
        self.setObjectName("output-form")

        main_layout = QtWidgets.QGridLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(8)

        self._sub_folder_form = SubFolderForm(self)
        self._sub_folder_form.setMinimumHeight(100)

        sub_folder_group = GroupFormWidget(
            self._sub_folder_form,
            vertical_stretch=False, parent=self
        )
        sub_folder_group.setTitle("Sub-Folder")
        main_layout.addWidget(sub_folder_group, 0, 0)

        self._file_name_form = FileNameForm(self)
        self._file_name_form.setMinimumHeight(100)

        file_name_group = GroupFormWidget(
            self._file_name_form,
            vertical_stretch=False, parent=self
        )
        file_name_group.setTitle("File Name")
        main_layout.addWidget(file_name_group, 0, 1)

        self._output_list = QtWidgets.QListWidget(self)
        self._output_list.setObjectName("output-list")
        self._output_list.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        main_layout.addWidget(self._output_list, 1, 0, 1, 2)
        main_layout.rowStretch(1)

        for node in sorted(nodes, key=lambda n: n.name()):
            output_form = OutputSettingsForm(node, blacklisted_names, self)
            output_widget = ListFormItemWidget(
                output_form, not node["disable"].value(), self
            )

            item = QtWidgets.QListWidgetItem()
            item.setSizeHint(output_widget.sizeHint())
            self._output_list.addItem(item)
            self._output_list.setItemWidget(item, output_widget)

    def _connect_signals(self):
        """Initialize signals connection."""


class SubFolderForm(QtWidgets.QWidget):
    """Form to manage sub-folders settings."""

    def __init__(self, parent=None):
        """Initiate the widget."""
        super(SubFolderForm, self).__init__(parent)
        self._setup_ui()

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

        self._create_now = QtWidgets.QCheckBox("Create sub-folders now", self)
        main_layout.addWidget(self._create_now, 2, 0, 1, 2)

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
