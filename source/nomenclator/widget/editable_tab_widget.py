# -*- coding: utf-8 -*-

from nomenclator.vendor.Qt import QtWidgets, QtCore

from .overlay_message import OverlayMessage


class EditableTabWidget(QtWidgets.QTabWidget):
    """Tab Widget with editable tabs."""

    #: :term:`Qt Signal` emitted when a new tab is requested.
    new_tab_requested = QtCore.Signal()

    #: :term:`Qt Signal` emitted when a tab is removed.
    tab_removed = QtCore.Signal(int)

    #: :term:`Qt Signal` emitted when a tab is edited.
    tab_edited = QtCore.Signal(int)

    def __init__(self, parent=None):
        """Initiate the widget."""
        super(EditableTabWidget, self).__init__(parent)
        self._setup_ui()
        self._connect_signals()

    def set_instruction(self, text):
        """Set *text* to display when no tab are added."""
        self._overlay_message.set_message(text)

    def _setup_ui(self):
        """Initialize user interface."""
        self.setTabBar(TabBar(self))
        self.setMovable(True)
        self.setTabsClosable(True)

        self._plus_button = QtWidgets.QToolButton(self)
        self._plus_button.setObjectName("editable-tab-widget")
        self._plus_button.setText("+")
        self._plus_button.setFixedSize(18, 18)
        self.setCornerWidget(self._plus_button)

        self._overlay_message = OverlayMessage(self)

    def _connect_signals(self):
        """Initialize signals connection."""
        self._plus_button.clicked.connect(self.new_tab_requested.emit)
        self.currentChanged.connect(self._toggle_message_overlay)
        self.tabCloseRequested.connect(self.removeTab)
        self.tabBar().tab_text_edited.connect(self.tab_edited.emit)

    def _toggle_message_overlay(self):
        """Hide the message overlay if tabs are added."""
        index = self.currentIndex()
        self._overlay_message.setVisible(index == -1)

    # noinspection PyPep8Naming
    def tabRemoved(self, index):
        """Handler called after a tab is removed from *index*.

        The :meth:`QTabWidget.tabRemoved` method is reimplemented to
        emit a signal when a tab is removed.

        """
        self.tab_removed.emit(index)
        super(EditableTabWidget, self).tabRemoved(index)
        self._toggle_message_overlay()

    # noinspection PyPep8Naming
    def resizeEvent(self, event):
        """Handle *event* when widget is being resized.

        The :meth:`QWidget.resizeEvent` method is reimplemented to
        ensure that overlay widget fully covers the widget.

        :param event: Instance of :class:`QtGui.QResizeEvent`

        """
        size = event.size() - QtCore.QSize(40, 0)
        self._overlay_message.resize(size)
        super(EditableTabWidget, self).resizeEvent(event)


class TabBar(QtWidgets.QTabBar):
    """Tab bar with editable labels."""

    #: :term:`Qt Signal` emitted when the label of a tab is edited.
    tab_text_edited = QtCore.Signal(int)

    def __init__(self, parent=None):
        """Initiate the widget."""
        super(TabBar, self).__init__(parent)
        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self):
        """Initialize user interface."""
        self._editor = QtWidgets.QLineEdit(self)
        self._editor.setWindowFlags(QtCore.Qt.Popup)
        self._editor.setFocusProxy(self)
        self._editor.installEventFilter(self)

    def _connect_signals(self):
        """Initialize signals connection."""
        self._editor.editingFinished.connect(self._handle_editing_finished)

    def _handle_editing_finished(self):
        """Persist the new tab label."""
        index = self.currentIndex()
        if index >= 0:
            self._editor.hide()
            self.setTabText(index, self._editor.text())
            self.tab_text_edited.emit(index)

    def edit_tab(self, index):
        """Edit tab label at targeted *index*."""
        rect = self.tabRect(index)
        self._editor.setFixedSize(rect.width() - 35, rect.height())
        self._editor.move(self.parent().mapToGlobal(rect.topLeft()))
        self._editor.setText(self.tabText(index))
        if not self._editor.isVisible():
            self._editor.show()

    # noinspection PyPep8Naming
    def mouseDoubleClickEvent(self, event):
        """Handle *event* when double-clicking on table.

        The :meth:`QWidget.mouseDoubleClickEvent` method is reimplemented
        to edit a tab label when double-clicking on it.

        :param event: Instance of :class:`QtGui.QMouseEvent`

        """
        index = self.tabAt(event.pos())
        if index >= 0:
            self.edit_tab(index)

    # noinspection PyPep8Naming
    def eventFilter(self, widget, event):
        """Filters events for this object.

        The :meth:`QObject.eventFilter` method is reimplemented
        to implement logic to hide editor.

        :param widget: Instance of :class:`QtCore.QObject`

        :param event: Instance of :class:`QtCore.QEvent`

        """
        click_outside_widget = (
            event.type() == QtCore.QEvent.MouseButtonPress
            and not self._editor.geometry().contains(event.globalPos())
        )

        press_escape = (
            event.type() == QtCore.QEvent.KeyPress
            and event.key() == QtCore.Qt.Key_Escape
        )

        if click_outside_widget or press_escape:
            self._editor.hide()
            return True

        return super(TabBar, self).eventFilter(widget, event)
