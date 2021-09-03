# -*- coding: utf-8 -*-

import re

from nomenclator.vendor.Qt import QtWidgets, QtCore


class TokenEditor(QtWidgets.QLineEdit):
    """Widget used to edit a token."""

    #: :term:`Qt Signal` emitted when value has been updated.
    updated = QtCore.Signal(str)

    def __init__(self, blacklist=None, parent=None):
        """Initiate the widget."""
        super(TokenEditor, self).__init__(parent)
        self._blacklist = blacklist or []
        self._connect_signals()

    def _connect_signals(self):
        """Initialize signals connection."""
        self.textChanged.connect(self._sanitize)
        self.editingFinished.connect(self._handle_finished_editing)

    def _sanitize(self, message):
        """Sanitize message by removing non alpha-numerical characters.
        """
        message = re.sub(r"[^a-zA-Z0-9]", "", message)

        self._update_text(message)

    def _handle_finished_editing(self):
        """Ensure that the final message is not blacklisted."""
        text = self.text()

        if text not in self._blacklist:
            return

        index = 1

        while "{}{}".format(text, index) in self._blacklist:
            index += 1

        self._update_text("{}{}".format(text, index))

    def _update_text(self, text):
        """Update text value  signals."""
        self.blockSignals(True)

        cursor_position = self.cursorPosition()
        self.setText(text)
        self.setCursorPosition(cursor_position)

        self.blockSignals(False)

        self.updated.emit(text)
