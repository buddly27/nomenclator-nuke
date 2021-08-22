# -*- coding: utf-8 -*-

from nomenclator.vendor.Qt import QtWidgets, QtCore, QtGui


class EditableList(QtWidgets.QWidget):
    """Widget representing a list with editable items."""

    def __init__(self, parent=None):
        """Initiate the widget."""
        super(EditableList, self).__init__(parent)
        self._setup_ui()
        self._connect_signals()

    def set_values(self, texts):
        """Initialize values."""
        self._list.add_texts(texts)

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
        self._add_btn.clicked.connect(lambda: self._list.add_text("", set_focus=True))
        self._delete_btn.clicked.connect(self._list.remove_selection)
        self._list.itemSelectionChanged.connect(self._toggle_delete_button)

    def _toggle_delete_button(self):
        """Indicate whether delete button should be enabled."""
        self._delete_btn.setEnabled(len(self._list.selectedItems()) > 0)


class ListWidget(QtWidgets.QListWidget):
    """Custom list widget."""

    def add_texts(self, texts):
        """Initialize text items."""
        for text in texts:
            self.add_text(text)

    def add_text(self, text, set_focus=False):
        """Initialize text item."""
        item = QtWidgets.QListWidgetItem(text)
        item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
        self.addItem(item)

        if set_focus:
            self.editItem(item)
            self.scrollToItem(item)

    def remove_selection(self):
        """Remove selected items."""
        for item in self.selectedItems():
            row = self.row(item)
            self.takeItem(row)

    # noinspection PyPep8Naming
    def mouseDoubleClickEvent(self, event):
        """Handle *event* when double-clicking on widget.

        The :meth:`QWidget.mouseDoubleClickEvent` method is reimplemented
        to emit a signal to create a new item if user double-click outside
        of any items.

        :param event: Instance of :class:`QtGui.QMouseEvent`

        """
        index = self.indexAt(event.pos())
        if not index.isValid():
            self.add_text("", set_focus=True)
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
        if event in [
            QtGui.QKeySequence.Delete,
            QtGui.QKeySequence.Backspace
        ]:
            self.remove_selection()
