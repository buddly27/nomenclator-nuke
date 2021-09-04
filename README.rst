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

**********
Installing
**********

Copy the Python module :file:`./source/nomenclator` into your personal :file:`~/.nuke` folder
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

*************
Documentation
*************

Full documentation, including installation and setup guides, can be found at
http://nomenclator-nuke.readthedocs.io/en/stable/
