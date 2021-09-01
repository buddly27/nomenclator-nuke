# -*- coding: utf-8 -*-

import os

from nomenclator.vendor.Qt import QtWidgets, QtCore


class PathWidget(QtWidgets.QWidget):
    """Widget displaying a path in a truncating way while letting the user
    see and select the full path when clicking on it.

    """

    def __init__(self, parent=None):
        """Initiate the widget."""
        super(PathWidget, self).__init__(parent)
        self._setup_ui()
        self._connect_signals()

        # Initiate path.
        self.set_path("")

    def path(self):
        """Return path."""
        return self._path_selectable.path()

    def set_path(self, path):
        """Set a path to display."""
        short_text = os.path.basename(path)
        self._path_display.set_short_text(short_text)
        self._path_selectable.setText(path)

    def _setup_ui(self):
        """Initialize user interface."""
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        label = QtWidgets.QLabel("Path", self)
        label.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter
        )
        layout.addWidget(label)

        self._path_display = PathWidgetDisplay(self)
        layout.addWidget(self._path_display)

        self._path_selectable = PathWidgetSelectable(self)
        self._path_selectable.setVisible(False)
        layout.addWidget(self._path_selectable)

    def _connect_signals(self):
        """Initialize signals connection."""
        self._path_display.double_clicked.connect(self._toggle_widget)
        self._path_selectable.mouse_left.connect(self._toggle_widget)

    def _toggle_widget(self):
        """Toggle the widget displayed depending on the sender."""
        if self.sender() == self._path_display:
            self._path_display.setVisible(False)
            self._path_selectable.setVisible(True)

        elif self.sender() == self._path_selectable:
            self._path_display.setVisible(True)
            self._path_selectable.setVisible(False)


class PathWidgetDisplay(QtWidgets.QTextEdit):
    """Widget displaying the truncated path only."""

    #: :term:`Qt Signal` emitted when mouse double-clicked on the widget.
    double_clicked = QtCore.Signal()

    def __init__(self, parent=None):
        """Initiate the widget."""
        super(PathWidgetDisplay, self).__init__(parent)
        self._tokens_from_position = {}
        self._tooltip = QtWidgets.QToolTip

        self._setup_ui()

    def set_short_text(self, path):
        """Display truncated *path*."""
        prefix = "<span style='color:#9e987c'>[location] / </span>"
        self.setText(prefix + path)

    def _setup_ui(self):
        """Initialize user interface."""
        self.setObjectName("path-widget")

        self.setMaximumHeight(22)
        self.setMinimumHeight(22)
        self.setMouseTracking(True)
        self.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.setFrameShadow(QtWidgets.QFrame.Plain)
        self.setLineWidth(0)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setReadOnly(True)
        self.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)

    def clear_tokens(self):
        """Clear all _query_token_mapping previously recorded."""
        self._tokens_from_position = {}

    def add_token(self, token, position):
        """Add a *token* to display for a particular *position* of the cursor."""
        self._tokens_from_position[position] = token

    # noinspection PyPep8Naming
    def mouseMoveEvent(self, event):
        """Handle *event* when mouse move within widget.

        The :meth:`QWidget.mouseMoveEvent` method is reimplemented
        to display tooltip with token corresponding to current cursor position.

        :param event: Instance of :class:`QtGui.QMouseEvent`

        """
        super(PathWidgetDisplay, self).mouseMoveEvent(event)

        cursor = self.cursorForPosition(event.pos())
        index = cursor.anchor()

        if len(self.toPlainText()) > index > 0:
            for position, tokenName in self._tokens_from_position.items():
                if position[0] <= index <= position[1]:
                    self._tooltip.showText(event.globalPos(), tokenName)
                    break

    # noinspection PyPep8Naming
    def mouseDoubleClickEvent(self, _):
        """Handle *event* when double-clicking on widget.

        The :meth:`QWidget.mouseDoubleClickEvent` method is reimplemented
        to emit a signal when user double-click on widget.

        """
        self.double_clicked.emit()


class PathWidgetSelectable(QtWidgets.QLineEdit):
    """Widget displaying the full path selectable."""

    #: :term:`Qt Signal` emitted when mouse left the widget.
    mouse_left = QtCore.Signal()

    def __init__(self, parent=None):
        """Initiate the widget."""
        super(PathWidgetSelectable, self).__init__(parent)
        self._setup_ui()

    def path(self):
        """Return path."""
        return self.text()

    def _setup_ui(self):
        """Initialize user interface."""
        self.setObjectName("path-widget")

        self.setMaximumHeight(22)
        self.setMinimumHeight(22)
        self.setReadOnly(True)

    # noinspection PyPep8Naming
    def leaveEvent(self, _):
        """Handle *event* when cursor leave the widget.

        The :meth:`QWidget.leaveEvent` method is reimplemented
        to emit a signal mouse leave the widget.

        """
        self.mouse_left.emit()
