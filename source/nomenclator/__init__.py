# -*- coding: utf-8 -*-

import nuke

from nomenclator.dialog import CompoManagerDialog

from ._version import __version__

#: Output classes which can be rendered.
OUTPUT_CLASSES = ("Write", "DeepWrite")


def open_comp_manager_dialog():
    """Open the dialog to manage composition script and render output paths.
    """
    output_nodes, remaining_node_names = fetch_outputs()

    descriptions = [
        "comp",
        "precomp",
        "roto",
        "cleanup",
    ]

    panel = CompoManagerDialog(output_nodes, remaining_node_names, descriptions)
    panel.exec_()


def open_project_manager_dialog():
    """Open the dialog to manage project.
    """
    pass


def open_output_manager_dialog():
    """Open the dialog to manage render output paths.
    """
    pass


def fetch_outputs():
    """Return a tuple with a list of output nodes and a list with remaining node names."""
    output_nodes = []
    remaining_names = []

    for node in nuke.allNodes(group=nuke.root()):
        if node.Class() in OUTPUT_CLASSES:
            output_nodes.append(node)
        else:
            remaining_names.append(node.name())

    return output_nodes, remaining_names
