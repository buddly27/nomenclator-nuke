# -*- coding: utf-8 -*-

from nomenclator.vendor.Qt import QtWidgets, QtCore


class GroupWidget(QtWidgets.QGroupBox):
    """Group Box embedding a widget."""

    def __init__(self, widget, parent=None):
        """Initiate the widget."""
        super(GroupWidget, self).__init__(parent)
        self._setup_ui(widget)

    def _setup_ui(self, widget):
        """Initialize user interface."""
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.addWidget(widget)

        widget.setParent(self)

    def expand_vertically(self, value):
        """Indicate whether the widget should expand vertically."""
        self.setSizePolicy(
            QtWidgets.QSizePolicy(
                QtWidgets.QSizePolicy.Preferred,
                QtWidgets.QSizePolicy.Minimum if value
                else QtWidgets.QSizePolicy.Maximum
            )
        )
