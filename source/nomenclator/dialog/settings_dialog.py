# -*- coding: utf-8 -*-

from nomenclator.vendor.Qt import QtWidgets, QtCore

from .theme import classic_style


class SettingsDialog(QtWidgets.QDialog):

    def __init__(self, config, parent=None):
        super(SettingsDialog, self).__init__(parent)
        self._setup_ui(config)
        self._connect_signals()

    def _setup_ui(self, config):
        """Initialize user interface."""
        self.setWindowTitle("Nomenclator - Settings")
        self.setMinimumWidth(900)

        self.setStyleSheet(classic_style())

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(5)

        self._tab_widget = QtWidgets.QTabWidget(self)
        self._tab_widget.addTab(StructureTab(config, self), "Folder Structure")
        self._tab_widget.addTab(QtWidgets.QWidget(), "Naming Convention")
        main_layout.addWidget(self._tab_widget)

        self._button_box = QtWidgets.QDialogButtonBox(self)
        self._button_box.setOrientation(QtCore.Qt.Horizontal)
        self._button_box.addButton("Apply", QtWidgets.QDialogButtonBox.AcceptRole)
        self._button_box.addButton("Cancel", QtWidgets.QDialogButtonBox.RejectRole)
        main_layout.addWidget(self._button_box)

    def _connect_signals(self):
        """Initialize signals connection."""
        self._button_box.accepted.connect(self.accept)
        self._button_box.rejected.connect(self.reject)


class StructureTab(QtWidgets.QWidget):

    def __init__(self, config, parent=None):
        super(StructureTab, self).__init__(parent)
        self._setup_ui(config)
        self._connect_signals()

    def _setup_ui(self, config):
        """Initialize user interface."""
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(5)

        root_layout = QtWidgets.QHBoxLayout()
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(5)

        root_label = QtWidgets.QLabel("Root Path", self)
        root_layout.addWidget(root_label)

        self._root = QtWidgets.QLineEdit(self)
        root_layout.addWidget(self._root)

        main_layout.addItem(root_layout)

        # self._tree_view = StructureTreeView(self)
        # main_layout.addWidget(self._tree_view)

    def _connect_signals(self):
        """Initialize signals connection."""
