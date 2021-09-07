.. _introduction:

************
Introduction
************

Nomenclator is a plugin for :term:`Nuke`, :term:`Nuke Studio` and :term:`Hiero` to save a
composition (.nk) or project (.hrox) scene and manage render outputs following a specific
naming convention based on the folder structure.

.. image:: ./image/demo.gif
    :alt: Demonstration

How does it work?
=================

Descriptive and consistent file names are an important part of organizing, sharing, and
keeping track of data files. File naming can be tedious and error prone, so it is
often a good idea to automate the process.

However, naming conventions are often based on elements that are specific to a project.
It would not make sense to adopt a similar convention for an episodic program and a commercial.
On top of that, studios often request a strict naming convention for content delivery, so a rigid
automation can be hard to adjust and maintain.

The goal of this plugin is to provide a configurable way to define naming conventions
based on the folder structure.

Let's consider the following configuration:

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

If the scene path directory is matching the pattern path for the "Episodic" template,
the corresponding tokens will be extracted in order to compute the scene name based on
the pattern base given.

The "Episodic" template also define two naming conventions for render outputs:
"comps" and "precomps".

