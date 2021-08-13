# -*- coding: utf-8 -*-

from nomenclator.vendor.Qt import QtWidgets, QtCore


class ErrorWidget(QtWidgets.QFrame):
    """Widget used to display an error message."""

    def __init__(self, parent=None):
        """Initiate the widget."""
        super(ErrorWidget, self).__init__(parent)


class WarningWidget(QtWidgets.QFrame):
    """Widget used to display an error message."""

    def __init__(self, parent=None):
        """Initiate the widget."""
        super(WarningWidget, self).__init__(parent)
