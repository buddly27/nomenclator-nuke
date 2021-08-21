# -*- coding: utf-8 -*-

from nomenclator.vendor.Qt import QtWidgets, QtCore, QtGui


class EditableList(QtWidgets.QWidget):
    """Widget representing a list with editable items."""

    def __init__(self, parent=None):
        """Initiate the widget."""
        super(EditableList, self).__init__(parent)
        self._setup_ui()
        self._connect_signals()

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
        self._delete_btn.setEnabled(False)
        button_layout.addWidget(self._delete_btn)

        main_layout.addItem(button_layout)

    def _connect_signals(self):
        """Initialize signals connection."""
        self._add_btn.clicked.connect(lambda: self.add_item(""))
        self._delete_btn.clicked.connect(self.remove_selection)
        self._list.itemSelectionChanged.connect(self._toggle_delete_button)
        self._list.creation_requested.connect(lambda: self.add_item(""))
        self._list.deletion_requested.connect(self.remove_selection)

    def _toggle_delete_button(self):
        """Indicate whether delete button should be enabled."""
        self._delete_btn.setEnabled(len(self._list.selectedItems()) > 0)

    def add_items(self, texts):
        """Add multiple items initialized with *texts*."""
        for text in texts:
            self.add_item(text, editing=False)

    def add_item(self, text, editing=True):
        """Add item initialized with *text*."""
        item = QtWidgets.QListWidgetItem(text)

        item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
        self._list.addItem(item)

        if editing:
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
    creation_requested = QtCore.Signal()

    #: :term:`Qt Signal` emitted when selected items must be deleted.
    deletion_requested = QtCore.Signal()

    # noinspection PyPep8Naming
    def mouseDoubleClickEvent(self, event):
        """Handle *event* when double-clicking on widget.

        The :meth:`QWidget.mouseDoubleClickEvent` method is reimplemented
        to emit a signal to create a new item if user double-click outside
        of any items.

        """
        index = self.indexAt(event.pos())
        if not index.isValid():
            self.creation_requested.emit()
            return

        super(ListWidget, self).mouseDoubleClickEvent(event)

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
            return

        super(ListWidget, self).mouseReleaseEvent(event)

    # noinspection PyPep8Naming
    def keyPressEvent(self, event):
        """Handle *event* when a key is pressed.

        The :meth:`QWidget.keyPressEvent` method is reimplemented to implement
        logic to delete selected items.

        :param event: Instance of :class:`QtGui.QKeyEvent`

        """
        if event in [QtGui.QKeySequence.Delete, QtGui.QKeySequence.Backspace]:
            self.deletion_requested.emit()
