# -*- coding: utf-8 -*-

from nomenclator.vendor.Qt import QtWidgets, QtCore

from .overlay_message import OverlayMessage


class EditableTabWidget(QtWidgets.QTabWidget):
    """Tab Widget with editable tabs."""

    def __init__(self, parent=None):
        """Initiate the widget."""
        super(EditableTabWidget, self).__init__(parent)
        self._setup_ui()
        self._connect_signals()

        self._tab_name = "Tab"
        self._constructor = QtWidgets.QWidget

    def set_instruction(self, text):
        """Set *text* to display when no tab are added."""
        self._overlay_message.set_message(text)

    def set_tab_name(self, text):
        """Set base name for new tab."""
        self._tab_name = text

    def set_widget_constructor(self, constructor):
        """Set constructor for new tab widgets."""
        self._constructor = constructor

    def _setup_ui(self):
        """Initialize user interface."""
        self.setTabBar(TabBar(self))
        self.setMovable(True)
        self.setTabsClosable(True)

        self._plus_button = QtWidgets.QToolButton(self)
        self._plus_button.setObjectName("editable-tab-widget")
        self._plus_button.setText("+")
        self._plus_button.setFixedSize(22, 20)
        self.setCornerWidget(self._plus_button)

        self._overlay_message = OverlayMessage(self)

    def _connect_signals(self):
        """Initialize signals connection."""
        self._plus_button.clicked.connect(self.add_tab)
        self.currentChanged.connect(self._toggle_message_overlay)
        self.tabCloseRequested.connect(self.removeTab)

    def add_tab(self):
        """Add a new tab."""
        name = "{0}{1}".format(self._tab_name, self.count() + 1)
        self.addTab(self._constructor(), name)

    def _toggle_message_overlay(self, index):
        """Hide the message overlay if tabs are added."""
        self._overlay_message.setVisible(index == -1)

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
