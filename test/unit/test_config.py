# -*- coding: utf-8 -*-

import os

import pytest


@pytest.fixture()
def mocked_expanduser(mocker, temporary_directory):
    """Return mocked 'os.path.expanduser' function."""
    return mocker.patch.object(os.path, "expanduser", return_value="__HOME__")


@pytest.fixture()
def mocked_path(mocker, temporary_directory):
    """Return mocked 'nomenclator.config.path' function."""
    import nomenclator.config
    return mocker.patch.object(nomenclator.config, "path")


@pytest.fixture()
def mocked_load(mocker, temporary_directory):
    """Return mocked 'nomenclator.config.load' function."""
    import nomenclator.config
    return mocker.patch.object(nomenclator.config, "load")


def test_path(mocked_expanduser, monkeypatch):
    """Return path to configuration file."""
    monkeypatch.delenv("NOMENCLATURE_CONFIG_PATH", raising=False)

    import nomenclator.config

    path = nomenclator.config.path()
    assert path == os.path.join("__HOME__", ".nuke", "nomenclator.toml")

    mocked_expanduser.assert_called_once_with("~")


def test_path_from_env(mocked_expanduser, monkeypatch):
    """Return path to configuration file fetch from environment"""
    monkeypatch.setenv("NOMENCLATURE_CONFIG_PATH", "__CONFIG__")

    import nomenclator.config

    path = nomenclator.config.path()
    assert path == os.path.join("__CONFIG__", "nomenclator.toml")

    mocked_expanduser.assert_called_once_with("~")


def test_fetch_empty(mocked_path, mocked_load):
    """Return empty configuration object."""
    import nomenclator.config

    mocked_path.return_value = "/path"

    config = nomenclator.config.fetch()
    assert config == mocked_load.return_value

    mocked_load.assert_called_once_with({})


def test_fetch(mocked_path, mocked_load, temporary_file):
    """Return configuration object."""
    import nomenclator.config

    with open(temporary_file, "w") as stream:
        stream.write(
            "descriptions = [\"comp\", \"precomp\", \"roto\"]\n"
            "create-subfolders = true\n"
            "\n"
            "[[comp-templates]]\n"
            "id = \"Default\"\n"
            "path = \"/path/{project}/{identity}/{shot}/scripts\"\n"
            "base-name = \"{identity}_{shot}_{description}_v{version}\"\n"
            "\n"
            "[[comp-templates.outputs]]\n"
            "id = \"Comp\"\n"
            "path = \"/path/{project}/{identity}/{shot}/comps\"\n"
            "base-name = \"{identity}_{shot}_comp_v{version}\"\n"
            "\n"
            "[[comp-templates.outputs]]\n"
            "id = \"Precomp\"\n"
            "path = \"/path/{project}/{identity}/{shot}/precomps\"\n"
            "base-name = \"{identity}_{shot}_precomp_v{version}\"\n"
            "\n"
            "[[comp-templates.outputs]]\n"
            "id = \"Roto\"\n"
            "path = \"/path/{project}/{identity}/{shot}/roto\"\n"
            "base-name = \"{identity}_{shot}_roto_v{version}\"\n"
        )

    mocked_path.return_value = temporary_file

    config = nomenclator.config.fetch()
    assert config == mocked_load.return_value

    mocked_load.assert_called_once_with({
        "descriptions": ["comp", "precomp", "roto"],
        "create-subfolders": True,
        "comp-templates": [
            {
                "id": "Default",
                "path": "/path/{project}/{identity}/{shot}/scripts",
                "base-name": "{identity}_{shot}_{description}_v{version}",
                "outputs": [
                    {
                        "id": "Comp",
                        "path": "/path/{project}/{identity}/{shot}/comps",
                        "base-name": "{identity}_{shot}_comp_v{version}",
                    },
                    {
                        "id": "Precomp",
                        "path": "/path/{project}/{identity}/{shot}/precomps",
                        "base-name": "{identity}_{shot}_precomp_v{version}",
                    },
                    {
                        "id": "Roto",
                        "path": "/path/{project}/{identity}/{shot}/roto",
                        "base-name": "{identity}_{shot}_roto_v{version}",
                    },
                ]
            }
        ]
    })
