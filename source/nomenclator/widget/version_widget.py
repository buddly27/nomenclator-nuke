# -*- coding: utf-8 -*-

from nomenclator.vendor.Qt import QtWidgets, QtCore


class VersionWidget(QtWidgets.QFrame):
    """Widget used to display version."""

    def __init__(self, parent=None):
        """Initiate the widget."""
        super(VersionWidget, self).__init__(parent)
        self._setup_ui()

    def set_value(self, version):
        """Initiate value."""
        if version is None:
            self._version_lbl.setText("...")
        else:
            version = "{0:03d}".format(version)
            self._version_lbl.setText(version)

    def _setup_ui(self):
        """Initialize user interface."""
        self.setObjectName("version-box")

        main_layout = QtWidgets.QHBoxLayout(self)
        main_layout.setSpacing(12)

        version_lbl = QtWidgets.QLabel("Version", self)
        version_lbl.setObjectName("version-label")

        self._version_lbl = QtWidgets.QLabel("...", self)
        self._version_lbl.setObjectName("version-value")

        main_layout.addWidget(version_lbl)
        main_layout.addWidget(self._version_lbl)
