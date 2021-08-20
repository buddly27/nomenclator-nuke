# -*- coding: utf-8 -*-

from nomenclator.vendor.Qt import QtWidgets, QtCore


class EditableList(QtWidgets.QWidget):

    def __init__(self, parent=None):
        """List with editable items."""
        super(EditableList, self).__init__(parent)
        self._setup_ui()
        self._connect_signals()

        self._toggle_delete_button()

    def _setup_ui(self):
        """Initialize user interface."""
        main_layout = QtWidgets.QGridLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(5)

        self._list = ListWidget(self)
        main_layout.addWidget(self._list)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(5)

        self._add_btn = QtWidgets.QPushButton("Add", self)
        button_layout.addWidget(self._add_btn)

        self._delete_btn = QtWidgets.QPushButton("Delete", self)
        button_layout.addWidget(self._delete_btn)

        main_layout.addItem(button_layout)

    def _connect_signals(self):
        """Initialize signals connection."""
        self._add_btn.clicked.connect(lambda: self.add(""))
        self._delete_btn.clicked.connect(self.remove_selection)
        self._list.itemSelectionChanged.connect(self._toggle_delete_button)
        self._list.new_item_requested.connect(lambda: self.add(""))

    def _toggle_delete_button(self):
        """Indicate whether delete button should be enabled."""
        self._delete_btn.setEnabled(len(self._list.selectedItems()) > 0)

    def add(self, text):
        """Add item initialized with *text*."""
        item = QtWidgets.QListWidgetItem(text)

        item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
        self._list.addItem(item)

        self._list.editItem(item)
        self._list.scrollToItem(item)

    def remove_selection(self):
        """Remove selected items."""
        for item in self._list.selectedItems():
            row = self._list.row(item)
            self._list.takeItem(row)


class ListWidget(QtWidgets.QListWidget):
    """Custom list widget."""

    #: :term:`Qt Signal` emitted when a new item must be created.
    new_item_requested = QtCore.Signal()

    # noinspection PyPep8Naming
    def mouseDoubleClickEvent(self, event):
        """Handle *event* when double-clicking on widget.

        The :meth:`QWidget.mouseDoubleClickEvent` method is reimplemented
        to emit a signal to create a new item if user double-click outside
        of any items.

        """
        index = self.indexAt(event.pos())
        if not index.isValid():
            self.new_item_requested.emit()

    # noinspection PyPep8Naming
    def mouseReleaseEvent(self, event):
        """Handle *event* when mouse is released from widget.

        The :meth:`QWidget.mouseReleaseEvent` method is reimplemented to
        ensure that a click outside of items clears the selection.

        :param event: Instance of :class:`QtGui.QMouseEvent`

        """
        index = self.indexAt(event.pos())
        if not index.isValid():
            self.selectionModel().clear()

