# -*- coding: utf-8 -*-

import os

from nomenclator.vendor.Qt import QtWidgets, QtCore


class LocationWidget(QtWidgets.QFrame):
    """Widget used to manage location path."""

    #: :term:`Qt Signal` emitted when location has been updated.
    updated = QtCore.Signal()

    def __init__(self, parent=None):
        """Initiate the widget."""
        super(LocationWidget, self).__init__(parent)
        self._setup_ui()
        self._connect_signals()

    @property
    def value(self):
        """Return current location."""
        return self._location.currentText()

    def set_items(self, recent_locations, current_path):
        """Initialize items."""
        if os.path.isfile(current_path):
            current_path = os.path.dirname(current_path)

        self._location.clear()
        self._location.addItems(recent_locations)
        self._location.setEditText(current_path)

    def _setup_ui(self):
        """Initialize user interface."""
        self.setObjectName("location-box")

        self.setSizePolicy(
            QtWidgets.QSizePolicy(
                QtWidgets.QSizePolicy.Preferred,
                QtWidgets.QSizePolicy.Maximum
            )
        )

        main_layout = QtWidgets.QHBoxLayout(self)

        label = QtWidgets.QLabel("Location", self)
        label.setMaximumWidth(70)
        self._location = QtWidgets.QComboBox(self)
        self._location.setEditable(True)
        self._completer = QtWidgets.QCompleter(self)
        self._completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self._completer.setCompletionMode(QtWidgets.QCompleter.InlineCompletion)
        model = QtWidgets.QDirModel(self._completer)
        model.setFilter(
            QtCore.QDir.Dirs | QtCore.QDir.NoDot | QtCore.QDir.NoDotDot
        )
        self._completer.setModel(model)
        self._location.setCompleter(self._completer)

        self._browse_btn = QtWidgets.QPushButton("Browse", self)
        self._browse_btn.setMaximumWidth(70)

        main_layout.addWidget(label)
        main_layout.addWidget(self._location)
        main_layout.addWidget(self._browse_btn)

    def _connect_signals(self):
        """Initialize signals connection."""
        self._browse_btn.clicked.connect(self.browse)
        self._location.currentIndexChanged.connect(lambda: self.updated.emit())
        self._location.editTextChanged.connect(lambda: self.updated.emit())

    def browse(self):
        """Open a browsing panel to choose the script location."""
        import nuke

        path = nuke.getFilename(
            "Please select a destination folder to save the script",
            default=self._location.currentText()
        )

        if path is not None:
            if os.path.isfile(path):
                path = os.path.dirname(path)

            self._location.setEditText(path)


