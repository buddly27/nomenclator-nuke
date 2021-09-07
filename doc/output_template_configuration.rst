.. _output_template_configuration:

*****************************
Output Template Configuration
*****************************

An output template configuration is a subset of a :ref:`template_configuration`
which define the naming convention for a render output video or image sequence.

.. _output_template_configuration/id:

id
==

Define the identifier of the output destination. It will be displayed
in the destination selector within the comp manager dialog.

.. code-block:: toml

    id = "comps"

.. _output_template_configuration/pattern-path:

pattern-path
============

Like the :ref:`template_configuration/pattern-path` option used for the
scene files, this option define the pattern of an output location path
compatible with the naming convention.

.. code-block:: toml

    pattern-path = "/path/{project}/{episode:ep\\d+}/{shot:sh\\d+}/comps"

.. _output_template_configuration/pattern-base:

pattern-base
============

Like the :ref:`template_configuration/pattern-base` option used for the
scene files, this option define the naming convention of the base of
a render output.

.. code-block:: toml

    pattern-base = "{project}_{episode}_{shot}_comp_v{version}"

.. _output_template_configuration/append-username-to-name:

append-username-to-name
=======================

Define whether the username should be appended to the render output file by
default.

.. code-block:: toml

    append-username-to-name = true

This feature is only available when the comp manager dialog is opened and
the current output file name is matching the template.

.. note::

    By default, this value is set to false.

.. _output_template_configuration/append-colorspace-to-name:

append-colorspace-to-name
=========================

Define whether the colorspace should be appended to the render output file by
default.

.. code-block:: toml

    append-colorspace-to-name = true

This feature is only available when the comp manager dialog is opened and
the current output file name is matching the template.

.. note::

    By default, this value is set to false.


.. _output_template_configuration/append-passname-to-name:

append-passname-to-name
=======================

Define whether the passname should be appended to the render output file by
default.

.. code-block:: toml

    append-passname-to-name = true

This feature is only available when the comp manager dialog is opened and
the current output file name is matching the template.

.. note::

    By default, this value is set to false.


.. _output_template_configuration/append-passname-to-subfolder:

append-passname-to-subfolder
============================

Define whether the passname should be appended to the render output
subfolder by default.

.. code-block:: toml

    append-passname-to-subfolder = true

This feature is only available when the comp manager dialog is opened and
the current output file name is matching the template.

.. note::

    This option is ignored if the corresponding
    :ref:`output_template_configuration/pattern-base` value does not
    define a subfolder.

.. note::

    By default, this value is set to false.
