# -*- coding: utf-8 -*-

from nomenclator.vendor.Qt import QtWidgets, QtCore, QtGui


class OverlayMessage(QtWidgets.QWidget):
    """Widget displaying an information message over another widget."""

    def __init__(self, parent=None):
        """Initialize table."""
        super(OverlayMessage, self).__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        """Initialize user interface with *message*."""
        self.setObjectName("overlay")

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self._label = QtWidgets.QLabel(self)
        self._label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self._label.setWordWrap(True)

        main_layout.addWidget(self._label)

    def set_message(self, text):
        """Set *text* to display."""
        self._label.setText(text)
