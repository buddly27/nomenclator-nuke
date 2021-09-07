.. _configuration:

*************
Configuration
*************

A :term:`Toml` configuration is used to define templates and default options.

The configuration file must be named :file:`nomenclator.toml`. It is located in
:file:`~/.nuke` or by using the :envvar:`NOMENCLATOR_CONFIG_PATH` environment variable.

The configuration can be edited via the Settings dialog:

.. image:: ./image/settings-dialog.png
    :alt: Settings Dialog

.. _configuration/default-padding:

default-padding
===============

Define default value for the ``{padding}`` token.

.. code-block:: toml

    default-padding = "###"

.. note::

    The default padding will be 1. It will use the Hash notation (#)
    or the printf notation (%01d) following the preferences.

.. _configuration/default-description:

default-description
===================

Define default value for the ``{description}`` token.

.. code-block:: toml

    default-description = "comp"

.. note::

    The default description will be the first item of the :ref:`descriptions
    <configuration/descriptions>` list.

.. _configuration/descriptions:

descriptions
============

Define all available values for the ``{description}`` token.

.. code-block:: toml

    descriptions = ["desc1", "desc2", "desc3"]

.. note::

    The default descriptions are "comp", "precomp", "roto" and "cleanup".

.. _configuration/create-subfolders:

create-subfolders
=================

Define whether sub-folders defined for render outputs must be created
when a naming convention is applied.

.. code-block:: toml

    create-subfolders = true

.. note::

    By default, sub-folders are not created when a naming
    convention is applied.

.. _configuration/comp-templates:

comp-templates
==============

Define the :ref:`template configurations <template_configuration>` available
to define the naming convention of a composition scene file (.nk) and associated
render outputs.

.. code-block:: toml

    [[comp-templates]]
    id = "Episodic"
    pattern-path = "/path/{project}/{episode:ep\\d+}/{shot:sh\\d+}/scripts"
    pattern-base = "{project}_{episode}_{shot}_{description}_v{version}"

    [[comp-templates.outputs]]
    id = "comps"
    pattern-path = "/path/{project}/{episode:ep\\d+}/{shot:sh\\d+}/comps"
    pattern-base = "{project}_{episode}_{shot}_comp_v{version}"

    [[comp-templates.outputs]]
    id = "precomps"
    pattern-path = "/path/{project}/{episode:ep\\d+}/{shot:sh\\d+}/precomps"
    pattern-base = "{project}_{episode}_{shot}_precomp_v{version}"

.. note::

    By default, no composition templates are set.

.. _configuration/project-templates:

project-templates
=================

Define the :ref:`template configurations <template_configuration>` available
to define the naming convention of a project file (.hrox).

.. code-block:: toml

    [[project-templates]]
    id = "Conform"
    pattern-path = "/path/{project}/edit/hiero"
    pattern-base = "{project}_{description}_v{version}"

.. note::

    By default, no project templates are set.

.. _configuration/colorspace-aliases:

colorspace-aliases
==================

Define all aliased to use for colorspace values returned by Nuke to
resolve the ``{colorspace}`` token.

.. code-block:: toml

    [colorspace-aliases]
    "Gamma1.8" = "gamma18"
    linear = "lin"
    sRGB = "srgb"

.. note::

    By default, the "lin" alias is defined for the "linear" value and
    the "srgb" alias is defined for the "sRGB" value.

.. _configuration/tokens:

tokens
======

Define any additional token values that could be found in templates.

.. code-block:: toml

    [tokens]
    foo = "bar"

.. note::

    If the token ``{foo}`` is found in any templates, it will be replaced
    by "bar" following this example. An error will be raised if no value is
    defined.

.. _configuration/max-locations:

max-locations
=============

Define the maximum number of recent locations to display in the comp
and project management dialog.

.. code-block:: toml

    max-locations = 10

.. note::

    By default, only 5 recent locations will be displayed.

.. seealso::

    * :func:`nomenclator.utilities.fetch_recent_comp_paths`
    * :func:`nomenclator.utilities.fetch_recent_project_paths`

.. _configuration/max-padding:

max-padding
===========

Define the maximum available value of padding for image sequences. It will
adjust the list of padding available in the comp and output management
dialogs.

.. code-block:: toml

    max-padding = 10

.. note::

    By default, the maximum value of padding is 5.

.. seealso::

    :func:`nomenclator.utilities.fetch_paddings`

.. _configuration/username:

username
========

Define the value for the ``{username}`` token.

.. code-block:: toml

    username = "steve"

.. note::

    The default username will be the value returned by
    :func:`getpass.getuser`.
