# -*- coding: utf-8 -*-

from nomenclator.vendor.Qt import QtWidgets, QtCore, QtGui


class EditableList(QtWidgets.QWidget):
    """Widget representing a list with editable items."""

    #: :term:`Qt Signal` emitted when items have changed.
    updated = QtCore.Signal(tuple)

    def __init__(self, parent=None):
        """Initiate the widget."""
        super(EditableList, self).__init__(parent)
        self._setup_ui()
        self._connect_signals()

    def set_values(self, texts):
        """Initialize values."""
        self._list.set_rows(texts)

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
        self._add_btn.clicked.connect(lambda: self._list.add_row("", set_focus=True))
        self._delete_btn.clicked.connect(self._list.remove_selection)
        self._list.itemSelectionChanged.connect(self._toggle_delete_button)
        self._list.updated.connect(self.updated.emit)

    def _toggle_delete_button(self):
        """Indicate whether delete button should be enabled."""
        self._delete_btn.setEnabled(len(self._list.selectedItems()) > 0)

    # noinspection PyPep8Naming
    def keyPressEvent(self, event):
        """Handle *event* when a key is pressed.

        The :meth:`QWidget.keyPressEvent` method is reimplemented
        to redo/undo commands.

        :param event: Instance of :class:`QtGui.QKeyEvent`

        """
        if event == QtGui.QKeySequence.Undo:
            self._list.undo()

        elif event == QtGui.QKeySequence.Redo:
            self._list.redo()


class ListWidget(QtWidgets.QListWidget):
    """Custom list widget."""

    #: :term:`Qt Signal` emitted when items have changed.
    updated = QtCore.Signal(tuple)

    def __init__(self, parent=None):
        """Initiate the widget."""
        super(ListWidget, self).__init__(parent)
        self._undo_stack = QtWidgets.QUndoStack(self)
        self._connect_signals()

        # Record text in current item to allow for undoable edit.
        self._current_text = ""

    def set_rows(self, texts):
        """Initialize rows with text items."""
        # This operation is not undoable on purpose.
        self.clear()

        for text in texts:
            item = self.create_item(text)
            self.addItem(item)

    def add_row(self, text, set_focus=False):
        """add new row with text item."""
        command = CommandInsert(self, text)
        self._undo_stack.push(command)

        if set_focus:
            item = self.item(command.row)

            self.editItem(item)
            self.scrollToItem(item)

    def remove_selection(self):
        """Remove selected items."""
        command = CommandDelete(self, self.selectedItems())
        self._undo_stack.push(command)

    @staticmethod
    def create_item(text):
        """Create editable item from *text*."""
        item = QtWidgets.QListWidgetItem(text)
        item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
        return item

    def _connect_signals(self):
        """Initialize signals connection."""
        self.itemChanged.connect(self._handle_change)
        self.currentItemChanged.connect(self._record_current_text)
        self._undo_stack.indexChanged.connect(self._emit_updated_signal)

    def _handle_change(self, item):
        """Handle recording of editing operation so that it can be undone."""
        command = CommandEdit(self, item, self._current_text)
        self._undo_stack.push(command)

    def _record_current_text(self, item):
        """Record edited item text so that operation can be undone."""
        self._current_text = item.text() if item is not None else ""

    def _emit_updated_signal(self):
        """Emit a signal with updated items."""
        items = [
            self.item(row).text() for row
            in range(self.count())
            if len(self.item(row).text())
        ]
        self.updated.emit(tuple(items))

    def undo(self):
        """Undo last command."""
        self._undo_stack.undo()

    def redo(self):
        """Redo last command."""
        self._undo_stack.redo()

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

        The :meth:`QWidget.keyPressEvent` method is reimplemented to add
        logic to delete items and redo/undo commands.

        :param event: Instance of :class:`QtGui.QKeyEvent`

        """
        if event in [
            QtGui.QKeySequence.Delete,
            QtGui.QKeySequence.Backspace
        ]:
            self.remove_selection()

        elif event == QtGui.QKeySequence.Undo:
            self._undo_stack.undo()

        elif event == QtGui.QKeySequence.Redo:
            self._undo_stack.redo()


class CommandEdit(QtWidgets.QUndoCommand):
    """Undoable command to edit an item on a list."""

    def __init__(self, widget, item, text_before):
        """Initiate the command."""
        super(CommandEdit, self).__init__()
        self._list = widget
        self._text_before = text_before
        self._text_after = item.text()
        self._row = self._list.row(item)

    def redo(self):
        """Execute or re-execute the command."""
        self._list.blockSignals(True)
        self._list.item(self._row).setText(self._text_after)
        self._list.setCurrentRow(self._row)
        self._list.blockSignals(False)

    def undo(self):
        """Reverse execution of the command."""
        self._list.blockSignals(True)
        self._list.item(self._row).setText(self._text_before)
        self._list.setCurrentRow(self._row)
        self._list.blockSignals(False)


class CommandInsert(QtWidgets.QUndoCommand):
    """Undoable command to insert items to a list."""

    def __init__(self, widget, text):
        """Initiate the command."""
        super(CommandInsert, self).__init__()
        self._list = widget
        self._row = self._list.count()
        self._text = text

    @property
    def row(self):
        """Return affected row."""
        return self._row

    def redo(self):
        """Execute or re-execute the command."""
        item = self._list.create_item(self._text)
        self._list.insertItem(self._row, item)
        self._list.setCurrentRow(self._row)

    def undo(self):
        """Reverse execution of the command."""
        self._list.takeItem(self._row)


class CommandDelete(QtWidgets.QUndoCommand):
    """Undoable command to delete items from a list."""

    def __init__(self, widget, items):
        """Initiate the command."""
        super(CommandDelete, self).__init__()
        self._list = widget
        self._values = [
            (self._list.row(item), item.text())
            for item in items
        ]

    @property
    def rows(self):
        """Return affected rows."""
        return [v[0] for v in self._values]

    def redo(self):
        """Execute or re-execute the command."""
        for row, _ in sorted(self._values, reverse=True):
            self._list.takeItem(row)

    def undo(self):
        """Reverse execution of the command."""
        for row, text in self._values:
            item = self._list.create_item(text)
            self._list.insertItem(row, item)
