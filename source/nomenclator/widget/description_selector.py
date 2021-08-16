# -*- coding: utf-8 -*-

import re

from nomenclator.vendor.Qt import QtWidgets, QtCore


class DescriptionSelector(QtWidgets.QWidget):
    """Widget used to select a description."""

    #: :term:`Qt Signal` emitted when description value has been updated.
    updated = QtCore.Signal()

    def __init__(self, descriptions, parent=None):
        """Initiate the widget."""
        super(DescriptionSelector, self).__init__(parent)
        self._items = list(descriptions) + ["-- custom --"]

        self._setup_ui()
        self._connect_signals()

    def value(self):
        """Return current value."""
        if self._description.currentIndex() == len(self._items) - 1:
            return self._custom_description.text()
        return self._description.currentText()

    def _setup_ui(self):
        """Initialize user interface."""
        main_layout = QtWidgets.QHBoxLayout(self)
        main_layout.setSpacing(8)
        main_layout.setContentsMargins(0, 0, 0, 0)

        label = QtWidgets.QLabel("Description", self)
        label.setMaximumWidth(80)
        label.setMinimumWidth(80)

        self._description = QtWidgets.QComboBox(self)
        self._description.addItems(self._items)
        self._custom_description = QtWidgets.QLineEdit(self)
        self._custom_description.setText("")
        self._custom_description.setVisible(False)

        spacer = QtWidgets.QSpacerItem(
            0, 0, QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Minimum
        )

        main_layout.addWidget(label)
        main_layout.addWidget(self._description)
        main_layout.addWidget(self._custom_description)
        main_layout.addItem(spacer)

    def _connect_signals(self):
        """Initialize signals connection."""
        self._description.currentIndexChanged.connect(self._update_ui)
        self._custom_description.textEdited.connect(self._sanitize)

    def _update_ui(self, index):
        """Update UI depending on the current *index* selected."""
        if index == len(self._items) - 1:
            self._custom_description.setVisible(True)
            self._custom_description.setFocus()

        else:
            self._custom_description.setVisible(False)

        self.updated.emit()

    def _sanitize(self, message):
        """Sanitize custom description by removing non alpha-numerical characters.
        """
        message = re.sub(r"[^a-zA-Z0-9]", "", message)

        self._custom_description.blockSignals(True)

        cursor_position = self._custom_description.cursorPosition()
        self._custom_description.setText(message)
        self._custom_description.setCursorPosition(cursor_position)

        self._custom_description.blockSignals(False)

        self.updated.emit()





