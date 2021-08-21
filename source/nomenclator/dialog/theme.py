# -*- coding: utf-8 -*-

import textwrap


def classic_style():
    """initiate CSS theme."""
    return textwrap.dedent(
        """
        QDialog {
            background: #282828;
        }
        QGroupBox {
            background: #333;
            border: 1px solid #151515;
            border-radius: 5px;
            padding-top: 25px;
        }
        QGroupBox::title {
            background: #151515;
            color: #ced5bb;
            border-bottom-right-radius: 5px;
            border-top-left-radius: 5px;
            font-size: 14px;
            font-weight: bold;
            subcontrol-origin: margin;
            subcontrol-position: top left;
            padding: 5px;
        }
        QScrollBar {
            border: 0;
            border-radius: 6px;
            background-color: #333;
            margin: 1px;
        }
        QScrollBar::handle { background: #222; border: 1px solid #111; }
        QScrollBar::sub-line, QScrollBar::add-line { height: 0px; width: 0px; }
        QWidget#output-form QListView {
            padding: 0px; border: 2px solid #222;
            border-radius: 3px; background: #555;
        }
        QWidget#output-form QListView::item { background: #555; }
        QWidget#output-form QGroupBox {
            background: #282828;
            border: 1px solid #222;
            border-radius: 5px;
            padding-top: 25px;
        }
        QWidget#output-form QGroupBox::title {
            background: #181818;
            color: #e3e8d7;
            border-bottom-right-radius: 5px;
            border-top-left-radius: 5px;
            font-size: 14px; font-weight: bold;
            subcontrol-origin: margin;
            subcontrol-position: top left;
            padding: 5px;
        }
        QFrame#location-box{
            background: #151515;
            border:0px;
        }
        QFrame#version-box {
            background: #222;
            border: 0x;
            border-radius: 5px;
            padding: 5px;
        }
        QLabel#version-label {
            padding: 0px;
            font-size: 14px;
        }
        QLabel#version-value {
            padding: 0px;
            font-size: 14px;
            color: #de8888;
            font-weight: bold;
        }
        QTextEdit#path-widget {
            color: #fff5c7;
            background: #323232;
            selection-background-color: #A66;
            selection-color: #fff5c7;
            border: 0px;
        }
        QTextEdit::disabled#path-widget {
            color: #9e987c;
            background: #323232;
            selection-background-color: #A66;
            selection-color: #fff5c7;
            border: 0px;
        }
        QLineEdit#path-widget {
            color: #fff5c7;
            background: #111;
            selection-background-color: #fff5c7;
            selection-color: #111;
            border: 0px;
            border-radius: 4px;
        }
        QFrame#list-item-selection {
            border-bottom-left-radius: 4px;
            border-top-left-radius: 4px;
            border: 1px solid #111;
            background: #111;
        }
        QFrame#list-item-form {
            border-bottom-right-radius: 4px;
            border-top-right-radius: 4px;
            border: 1px solid #111;
            background: #333;
        }
        QFrame#list-item-form QLabel {
            border: 0px;
            background: none;
        }
        QFrame#list-item-form QCheckBox {
            border: 0px;
            background: none;
        }
        QLineEdit {
            height: 20px;
        }
        QSpinBox {
            height: 25px;
        }
        QListView::item {
            height: 25px;
        }
        """
    )

