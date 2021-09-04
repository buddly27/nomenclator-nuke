################
Nomenclator Nuke
################

.. image:: https://github.com/buddly27/nomenclator-nuke/actions/workflows/main.yml/badge.svg
    :target: https://github.com/buddly27/nomenclator-nuke/actions/workflows/main.yml
    :alt: CI

.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
    :target: https://opensource.org/licenses/MIT
    :alt: License Link

.. image:: https://img.shields.io/badge/Nuke%20Versions-11.3%2012.0%2012.1%2012.2%2013.0-red
    :target: https://www.foundry.com/products/nuke
    :alt: Nuke Versions

Nuke plugin to name script and render outputs

.. image:: ./doc/image/demo.gif
    :alt: Demonstration

*******************
Installing for Nuke
*******************

Copy the Python module ``./source/nomenclator`` into your personal ``~/.nuke`` folder
(or update your NUKE_PATH environment variable) and add the following menu.py file:

.. code-block:: python

    import nuke

    import nomenclator

    menu_bar = nuke.menu("Nuke")
    menu = menu_bar.addMenu("&File")
    menu.addCommand("Nomenclator - Manage Comp...", nomenclator.open_comp_manager_dialog, index=0)
    menu.addCommand("Nomenclator - Manage Outputs...", nomenclator.open_output_manager_dialog, index=1)
    menu.addCommand("Nomenclator - Settings...", nomenclator.open_settings_dialog, index=2)
    menu.addSeparator(index=3)

see also: `Defining the Nuke Plug-in Path
<https://learn.foundry.com/nuke/content/comp_environment/configuring_nuke/defining_nuke_plugin_path.html>`_

*****************************
Installing for Hiero / Studio
*****************************

Copy the Python module ``./source/nomenclator`` into a ``~/.nuke/Python/StartupUI`` folder
(or update your HIERO_PLUGIN_PATH environment variable) and add the following menu.py file:

.. code-block:: python

    import hiero.ui

    import nomenclator
    from nomenclator.vendor.Qt import QtWidgets


    class ProjectManagerAction(QtWidgets.QAction):

        def __init__(self, parent=hiero.ui.mainWindow()):
            super(ProjectManagerAction, self).__init__("Nomenclator - Manage Project...", parent)
            self.triggered.connect(nomenclator.open_project_manager_dialog)


    class SettingsAction(QtWidgets.QAction):

        def __init__(self, parent=hiero.ui.mainWindow()):
            super(SettingsAction, self).__init__("Nomenclator - Settings...", parent)
            self.triggered.connect(nomenclator.open_settings_dialog)


    action = hiero.ui.findMenuAction("foundry.menu.file")
    menu = action.menu()

    separator = menu.insertSeparator(menu.actions()[0])
    menu.insertAction(separator, ProjectManagerAction())
    menu.insertAction(separator, SettingsAction())


see also: `Hiero Environment Setup
<https://learn.foundry.com/hiero/developers/latest/HieroPythonDevGuide/setup.html>`_

*************
Documentation
*************

Full documentation, including installation and setup guides, can be found at
http://nomenclator-nuke.readthedocs.io/en/stable/
