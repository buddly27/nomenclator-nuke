# -*- coding: utf-8 -*-

from nomenclator.vendor.Qt import QtWidgets, QtCore


class ListFormItemWidget(QtWidgets.QWidget):
    """Widget embedding a form widget within a list"""

    def __init__(self, form_widget, enabled, parent=None):
        """Initiate the widget."""
        super(ListFormItemWidget, self).__init__(parent)
        self._setup_ui(form_widget)
        self._connect_signals()

        # Initiate state
        self._selection.setCheckState(
            QtCore.Qt.Checked if enabled else QtCore.Qt.Unchecked
        )
        self._toggle_enable()

    def _setup_ui(self, form_widget):
        """Initialize user interface."""

        main_layout = QtWidgets.QHBoxLayout(self)
        main_layout.setContentsMargins(8, 8, 8, 0)
        main_layout.setSpacing(0)

        self._selection_frame = QtWidgets.QFrame(self)
        self._selection_frame.setObjectName("list-item-selection")
        selection_frame_layout = QtWidgets.QVBoxLayout(self._selection_frame)
        selection_frame_layout.setContentsMargins(5, 5, 5, 5)

        self._selection = QtWidgets.QCheckBox(self._selection_frame)
        selection_frame_layout.addWidget(self._selection)

        main_layout.addWidget(self._selection_frame)

        self._main_frame = QtWidgets.QFrame(self)
        self._main_frame.setObjectName("list-item-form")
        main_frame_layout = QtWidgets.QVBoxLayout(self._main_frame)
        main_frame_layout.setContentsMargins(5, 5, 5, 5)

        form_widget.setParent(self._main_frame)
        main_frame_layout.addWidget(form_widget)

        main_layout.addWidget(self._main_frame)

    def _connect_signals(self):
        """Initialize signals connection."""
        self._selection.stateChanged.connect(self._toggle_enable)

    def _toggle_enable(self):
        """Toggle the enabling state of the output widget."""
        self._main_frame.setEnabled(self._selection.isChecked())
