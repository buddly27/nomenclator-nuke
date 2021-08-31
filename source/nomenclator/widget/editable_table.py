# -*- coding: utf-8 -*-

from nomenclator.vendor.Qt import QtWidgets, QtCore, QtGui


class EditableTable(QtWidgets.QWidget):
    """Widget representing a table with editable items."""

    #: :term:`Qt Signal` emitted when items have changed.
    updated = QtCore.Signal(list)

    def __init__(self, headers, parent=None):
        """Initiate the widget."""
        super(EditableTable, self).__init__(parent)
        self._setup_ui(headers)
        self._connect_signals()

        self._table.setRowCount(1)

        item1 = QtWidgets.QTableWidgetItem("Item1")
        self._table.setItem(0, 0, item1)

    def set_values(self, texts):
        """Initialize values."""

    def _setup_ui(self, headers):
        """Initialize user interface."""
        main_layout = QtWidgets.QGridLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(5)

        self._table = TableWidget(headers, self)
        main_layout.addWidget(self._table)

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
        self._add_btn.clicked.connect(self._add_new_row)
        self._delete_btn.clicked.connect(self._table.remove_selection)
        self._table.itemSelectionChanged.connect(self._toggle_delete_button)

    def _add_new_row(self):
        """Add a new row when requested."""
        texts = ["" for _ in range(self._table.columnCount())]
        self._table.add_row(texts, set_focus=True)

    def _toggle_delete_button(self):
        """Indicate whether delete button should be enabled."""
        self._delete_btn.setEnabled(len(self._table.selectedItems()) > 0)


class TableWidget(QtWidgets.QTableWidget):
    """Custom table widget."""

    #: :term:`Qt Signal` emitted when items have changed.
    updated = QtCore.Signal(list)

    def __init__(self, headers, parent=None):
        """Initiate the widget."""
        super(TableWidget, self).__init__(parent)
        self._undo_stack = QtWidgets.QUndoStack(self)
        self._setup_ui(headers)
        self._connect_signals()

        # Record text in current item to allow for undoable edit.
        self._current_text = ""

    def _setup_ui(self, headers):
        """Initialize user interface."""
        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)
        self.setShowGrid(True)
        self.horizontalHeader().setStretchLastSection(True)
        self.verticalHeader().setVisible(False)
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

    def set_rows(self, row_items):
        """Initialize rows with text items."""
        # This operation is not undoable on purpose.
        self.clear()

        self.setRowCount(row_items)

        for row, texts in enumerate(row_items):
            for column, text in enumerate(texts):
                item = self.create_item(text or "")
                self.setItem(row, column, item)

    def add_row(self, texts, set_focus=False):
        """add new row with text items."""
        command = CommandInsert(self, texts)
        self._undo_stack.push(command)

        if set_focus:
            item = self.item(command.row, 0)

            self.editItem(item)
            self.scrollToItem(item)

    def remove_selection(self):
        """Remove selected items."""
        command = CommandDelete(self, self.selectedItems())
        self._undo_stack.push(command)

    @staticmethod
    def create_item(text):
        """Create editable item from *text*."""
        item = QtWidgets.QTableWidgetItem(text)
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
        # self.updated.emit(self.texts())

    def undo(self):
        """Undo last command."""
        self._undo_stack.undo()

    def redo(self):
        """Redo last command."""
        self._undo_stack.redo()

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
    """Undoable command to edit an item on a table."""

    def __init__(self, widget, item, text_before):
        """Initiate the command."""
        super(CommandEdit, self).__init__()
        self._table = widget
        self._text_before = text_before
        self._text_after = item.text() or ""
        self._row = self._table.row(item)
        self._column = self._table.column(item)

    def redo(self):
        """Execute or re-execute the command."""
        self._table.blockSignals(True)
        self._table.item(self._row, self._column).setText(self._text_after)
        self._table.setCurrentCell(self._row, self._column)
        self._table.blockSignals(False)

    def undo(self):
        """Reverse execution of the command."""
        self._table.blockSignals(True)
        self._table.item(self._row, self._column).setText(self._text_before)
        self._table.setCurrentCell(self._row, self._column)
        self._table.blockSignals(False)


class CommandInsert(QtWidgets.QUndoCommand):
    """Undoable command to insert items to a table."""

    def __init__(self, widget, texts):
        """Initiate the command."""
        super(CommandInsert, self).__init__()
        self._table = widget
        self._row = self._table.rowCount()
        self._texts = texts

    @property
    def row(self):
        """Return affected row."""
        return self._row

    def redo(self):
        """Execute or re-execute the command."""
        initial_count = self._table.rowCount()
        self._table.setRowCount(initial_count + 1)

        for column, text in enumerate(self._texts):
            item = self._table.create_item(text or "")
            self._table.setItem(self._row, column, item)

    def undo(self):
        """Reverse execution of the command."""
        self._table.removeRow(self._row)


class CommandDelete(QtWidgets.QUndoCommand):
    """Undoable command to delete items from a table."""

    def __init__(self, widget, items):
        """Initiate the command."""
        super(CommandDelete, self).__init__()
        self._table = widget

        self._value_mapping = {}

        for item in items:
            row = self._table.row(item)
            column = self._table.column(item)

            self._value_mapping.setdefault(row, {})
            self._value_mapping[row][column] = item.text()

    @property
    def rows(self):
        """Return affected rows."""
        return list(self._value_mapping.keys())

    def redo(self):
        """Execute or re-execute the command."""
        for row in sorted(self._value_mapping.keys(), reverse=True):
            self._table.removeRow(row)

    def undo(self):
        """Reverse execution of the command."""
        initial_count = self._table.rowCount()
        total = len(self._value_mapping.keys())
        self._table.setRowCount(initial_count + total)

        for row, mapping in sorted(self._value_mapping.items()):
            for column, text in sorted(mapping.items()):
                item = self._table.create_item(text or "")
                self._table.setItem(row, column, item)
