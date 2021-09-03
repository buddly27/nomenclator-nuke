# -*- coding: utf-8 -*-

from nomenclator.vendor.Qt import QtWidgets, QtCore


class ErrorManagerWidget(QtWidgets.QFrame):
    """Widget used to display error messages."""

    def __init__(self, parent=None):
        """Initiate the widget."""
        super(ErrorManagerWidget, self).__init__(parent)
        self._setup_ui()
        self._connect_signals()

        self._errors = []

    def set_values(self, context):
        """Initialize values."""
        errors = []
        included = set()

        if context.error is not None:
            errors.append(context.error)
            included.add(context.error["message"])

        for _context in context.outputs:
            if not _context.error:
                continue

            # Ignore duplicated error messages.
            if _context.error["message"] in included:
                continue

            errors.append(_context.error)
            included.add(_context.error["message"])

        # Ignore if error didn't change
        if errors == self._errors:
            return

        self.clear()

        for error in errors:
            widget = ErrorWidget(error)
            self._main_layout.addWidget(widget)

        self.setVisible(self._main_layout.count() > 0)
        self._errors = errors

    def clear(self):
        """Clear all error displayed."""
        for index in reversed(range(self._main_layout.count())):
            self._main_layout.itemAt(index).widget().deleteLater()

    def _setup_ui(self):
        """Initialize user interface."""
        self._main_layout = QtWidgets.QVBoxLayout(self)
        self._main_layout.setContentsMargins(0, 0, 0, 0)
        self._main_layout.setSpacing(0)

        self.setVisible(False)

    def _connect_signals(self):
        """Initialize signals connection."""


class ErrorWidget(QtWidgets.QFrame):
    """Widget used to display one message."""

    def __init__(self, error, parent=None):
        """Initiate the widget."""
        super(ErrorWidget, self).__init__(parent)
        self._setup_ui(error)
        self._connect_signals()

    def _setup_ui(self, error):
        """Initialize user interface."""
        self.setObjectName("error-widget")

        self.setSizePolicy(
            QtWidgets.QSizePolicy(
                QtWidgets.QSizePolicy.Preferred,
                QtWidgets.QSizePolicy.Maximum
            )
        )

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self._header = HeaderMessage(error["message"], self)
        main_layout.addWidget(self._header)

        self._detail = DetailsMessage(error["details"], self)
        main_layout.addWidget(self._detail)

    def _connect_signals(self):
        """Initialize signals connection."""
        self._header.request_details.connect(self._detail.display)


class HeaderMessage(QtWidgets.QFrame):
    """Widget used to display a header message."""

    #: :term:`Qt Signal` emitted when detail message is requested.
    request_details = QtCore.Signal(bool)

    def __init__(self, message, parent=None):
        """Initiate the widget."""
        super(HeaderMessage, self).__init__(parent)
        self._setup_ui(message)
        self._connect_signals()

    def _setup_ui(self, message):
        """Initialize user interface."""
        self.setObjectName("error-header-widget")

        self.setSizePolicy(
            QtWidgets.QSizePolicy(
                QtWidgets.QSizePolicy.Preferred,
                QtWidgets.QSizePolicy.Maximum
            )
        )

        main_layout = QtWidgets.QHBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(5)

        label = QtWidgets.QLabel("ERROR", self)
        label.setStyleSheet("font:bold")
        label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        label.setTextInteractionFlags(
            QtCore.Qt.LinksAccessibleByMouse | QtCore.Qt.TextSelectableByMouse
        )
        label.setMaximumWidth(80)
        label.setMinimumWidth(80)
        main_layout.addWidget(label)

        message_lbl = QtWidgets.QLabel(message, self)
        message_lbl.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        message_lbl.setTextInteractionFlags(
            QtCore.Qt.LinksAccessibleByMouse | QtCore.Qt.TextSelectableByMouse
        )
        main_layout.addWidget(message_lbl)

        spacer = QtWidgets.QSpacerItem(
            0, 0, QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Minimum
        )
        self._button_more = QtWidgets.QToolButton(self)
        self._button_more.setText("display more")

        main_layout.addItem(spacer)
        main_layout.addWidget(self._button_more)

    def _connect_signals(self):
        """Initialize signals connection."""
        self._button_more.clicked.connect(self._toggle_display)

    def _toggle_display(self):
        """Toggle the display of the message."""
        values = ["display more", "display less"]
        new_value = self._button_more.text() == values[0]
        self._button_more.setText(values[int(new_value)])
        self.request_details.emit(new_value)


class DetailsMessage(QtWidgets.QFrame):
    """Widget used to display a details message."""

    def __init__(self, message, parent=None):
        """Initiate the widget."""
        super(DetailsMessage, self).__init__(parent)
        self._setup_ui(message)

    def _setup_ui(self, message):
        """Initialize user interface."""
        main_layout = QtWidgets.QHBoxLayout(self)
        main_layout.setContentsMargins(90, 10, 10, 10)

        message_lbl = QtWidgets.QLabel(message, self)
        message_lbl.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        message_lbl.setTextInteractionFlags(
            QtCore.Qt.LinksAccessibleByMouse | QtCore.Qt.TextSelectableByMouse
        )
        message_lbl.setWordWrap(True)
        main_layout.addWidget(message_lbl)

        self.setVisible(False)

    def display(self, value):
        """indicate whether the widget should be visible"""
        self.setVisible(value)
