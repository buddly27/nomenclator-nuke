# -*- coding: utf-8 -*-

from nomenclator.vendor.Qt import QtWidgets

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
        self._file_name_form.set_values(context)

        for node in sorted(context["nodes"], key=lambda n: n.name()):
            self._output_list.add(node)

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

    def set_values(self, context):
        """Initialize values."""
        self._padding.addItems(context["paddings"])

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
