# -*- coding: utf-8 -*-

from nomenclator.vendor.Qt import QtWidgets, QtCore
from nomenclator.widget import LocationWidget
from nomenclator.widget import GroupFormWidget

from nomenclator.form import CompSettingsForm
from nomenclator.form import OutputsSettingsForm

from .theme import classic_style


class CompoManagerDialog(QtWidgets.QDialog):

    def __init__(self, options, parent=None):
        super(CompoManagerDialog, self).__init__(parent)
        self._setup_ui(options)
        self._connect_signals()

    def _setup_ui(self, options):
        """Initialize user interface."""
        self.setWindowTitle("Nomenclator - Composition Manager")
        self.setMinimumWidth(1100)

        self.setStyleSheet(classic_style())

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self._location = LocationWidget(self)
        main_layout.addWidget(self._location)

        body_layout = QtWidgets.QVBoxLayout()
        body_layout.setContentsMargins(10, 10, 10, 10)
        body_layout.setSpacing(8)

        self._comp_settings_form = CompSettingsForm(options, self)

        comp_settings_group = GroupFormWidget(
            self._comp_settings_form,
            vertical_stretch=False, parent=self
        )
        comp_settings_group.setTitle("Composition")
        comp_settings_group.setSizePolicy(
            QtWidgets.QSizePolicy(
                QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum
            )
        )
        body_layout.addWidget(comp_settings_group)

        self._outputs_settings_form = OutputsSettingsForm(options, self)

        outputs_settings_group = GroupFormWidget(
            self._outputs_settings_form,
            vertical_stretch=True, parent=self
        )
        outputs_settings_group.setTitle("Render Outputs")
        outputs_settings_group.setEnabled(len(options.nodes) > 0)
        body_layout.addWidget(outputs_settings_group)

        self._button_box = QtWidgets.QDialogButtonBox(self)
        self._button_box.setOrientation(QtCore.Qt.Horizontal)
        self._button_box.addButton("Apply", QtWidgets.QDialogButtonBox.AcceptRole)
        self._button_box.addButton("Cancel", QtWidgets.QDialogButtonBox.RejectRole)
        body_layout.addWidget(self._button_box)

        main_layout.addItem(body_layout)

    def _connect_signals(self):
        """Initialize signals connection."""
        self._button_box.accepted.connect(self.accept)
        self._button_box.rejected.connect(self.reject)
