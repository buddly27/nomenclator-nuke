.. _installing:

**********
Installing
**********

.. highlight:: bash

.. note::

    Using :term:`Virtualenv` is recommended when evaluating or running locally.

Installation is simple with `pip <http://www.pip-installer.org/>`__::

    pip install nomenclator-nuke

.. _installing/source:

Installing from source
======================

You can also install manually from the source for more control. First obtain a
copy of the source by either downloading the `zipball
<https://github.com/buddly27/nomenclator-nuke/archive/main.zip>`_
or cloning the public repository::

    git clone git@github.com:buddly27/nomenclator-nuke.git

Then you can build and install the package into your current Python
environment::

    pip install .

If actively developing, you can perform an editable install that will link to
the project source and reflect any local changes made instantly::

    pip install -e .

.. note::

    If you plan on building documentation and running tests, run the following
    command instead to install required extra packages for development::

        pip install -e ".[dev]"

Alternatively, just build locally and manage yourself::

    python setup.py build

.. _installing/source/doc:

Building documentation from source
----------------------------------

Ensure you have installed the 'extra' packages required for building the
documentation::

    pip install -e ".[doc]"

Then you can build the documentation with the command::

    python setup.py build_sphinx

View the result in your browser at::

    file:///path/to/nomenclator-nuke/build/doc/html/index.html

.. _installing/source/test:

Running tests against the source
--------------------------------

Ensure you have installed the 'extra' packages required for running the tests::

    pip install -e ".[test]"

Then run the tests as follows::

    python setup.py -q test

You can also generate a coverage report when running tests::

    python setup.py -q test --addopts "--cov --cov-report=html"

View the generated report at::

    file:///path/to/nomenclator-nuke/htmlcov/index.html


.. _installing/nuke:

Installing for Nuke
====================

Copy the Python module :file:`./source/nomenclator` into your personal :file:`~/.nuke` folder
(or update your :envvar:`NUKE_PATH` environment variable) and add the following
`menu.py` file:

.. code-block:: python

    import nuke

    import nomenclator

    menu_bar = nuke.menu("Nuke")
    menu = menu_bar.addMenu("&File")
    menu.addCommand("Nomenclator - Manage Comp...", nomenclator.open_comp_manager_dialog, index=0)
    menu.addCommand("Nomenclator - Manage Outputs...", nomenclator.open_output_manager_dialog, index=1)
    menu.addCommand("Nomenclator - Settings...", nomenclator.open_settings_dialog, index=2)
    menu.addSeparator(index=3)

This is how the menu should look like within Nuke:

.. image:: ./image/nuke-menu.png
    :alt: Nuke Menu

.. note::

    see also: `Defining the Nuke Plug-in Path
    <https://learn.foundry.com/nuke/content/comp_environment/
    configuring_nuke/defining_nuke_plugin_path.html>`_

.. _installing/hiero:

Installing for Hiero / Studio
=============================

Copy the Python module :file:`./source/nomenclator` into a :file:`~/.nuke/Python/StartupUI` folder
(or update your :envvar:`HIERO_PLUGIN_PATH` environment variable) and add the following
`menu.py` file:

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

This is how the menu should look like within Hiero or Nuke Studio:

.. image:: ./image/studio-menu.png
    :alt: Nuke Menu

.. note::

    see also: `Hiero Environment Setup
    <https://learn.foundry.com/hiero/developers/latest/HieroPythonDevGuide/setup.html>`_

.. _installing/external:

External dependencies
=====================

The plugin rely on two external dependencies:

* `toml <https://pypi.org/project/toml/>`_ to read :term:`Toml` configuration files.
* `Qt.py <https://pypi.org/project/Qt.py/>`_ to preserve compatibility between
  :term:`PySide` (used in Nuke 11 and earlier) and :term:`PySide2` (used in Nuke 12 and later).

For convenience, specific versions of these libraries are embedded in the plugin using
the `vendoring <https://pypi.org/project/vendoring/>`_ CLI tool. These versions are defined in
the :file:`source/nomenclator/vendor/vendor.txt` file:

.. include:: ../source/nomenclator/vendor/vendor.txt
   :code: ini

To update the versions, modify this file and run the following command::

    vendoring update .
