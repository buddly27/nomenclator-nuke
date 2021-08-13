# -*- coding: utf-8 -*-

from nomenclator.vendor.Qt import QtWidgets, QtCore


class GroupFormWidget(QtWidgets.QGroupBox):
    """Group Box embedding a form widget."""

    def __init__(self, form_widget, vertical_stretch, parent=None):
        """Initiate the widget."""
        super(GroupFormWidget, self).__init__(parent)
        self._setup_ui(form_widget, vertical_stretch)

    def _setup_ui(self, form_widget, vertical_stretch):
        """Initialize user interface."""
        self.setSizePolicy(
            QtWidgets.QSizePolicy(
                QtWidgets.QSizePolicy.Preferred,
                QtWidgets.QSizePolicy.Minimum if vertical_stretch
                else QtWidgets.QSizePolicy.Maximum
            )
        )

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.addWidget(form_widget)

        form_widget.setParent(self)
