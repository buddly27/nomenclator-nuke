# -*- coding: utf-8 -*-

import collections
import getpass
import os

import pytest


@pytest.fixture()
def mock_getuser(mocker):
    """Mock 'getpass.getuser' function."""
    return mocker.patch.object(getpass, "getuser", return_value="john-doe")


@pytest.fixture()
def mocked_expanduser(mocker):
    """Return mocked 'os.path.expanduser' function."""
    return mocker.patch.object(os.path, "expanduser", return_value="__HOME__")


@pytest.fixture()
def mocked_toml_load(mocker):
    """Return mocked 'nomenclator.vendor.toml.load' function."""
    import nomenclator.vendor.toml
    return mocker.patch.object(nomenclator.vendor.toml, "load")


@pytest.fixture()
def mocked_toml_dump(mocker):
    """Return mocked 'nomenclator.vendor.toml.dump' function."""
    import nomenclator.vendor.toml
    return mocker.patch.object(nomenclator.vendor.toml, "dump")


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


@pytest.fixture()
def mocked_dump(mocker, temporary_directory):
    """Return mocked 'nomenclator.config.dump' function."""
    import nomenclator.config
    return mocker.patch.object(nomenclator.config, "dump")


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


def test_fetch(mocked_path, mocked_load, temporary_file, mocked_toml_load):
    """Return configuration object."""
    import nomenclator.config

    mocked_path.return_value = temporary_file

    config = nomenclator.config.fetch()
    assert config == mocked_load.return_value

    mocked_load.assert_called_once_with(mocked_toml_load.return_value)
    mocked_path.assert_called_once()

    stream = mocked_toml_load.call_args_list[0][0][0]
    assert stream.mode == "r"
    assert stream.name == temporary_file


def test_save(mocker, mocked_path, mocked_dump, temporary_file, mocked_toml_dump):
    """Save configuration object."""
    import nomenclator.config

    mocked_path.return_value = temporary_file

    nomenclator.config.save("__CONFIG__")

    mocked_dump.assert_called_once_with("__CONFIG__")
    mocked_toml_dump.assert_called_once_with(
        mocked_dump.return_value, mocker.ANY
    )

    stream = mocked_toml_dump.call_args_list[0][0][1]
    assert stream.mode == "w"
    assert stream.name == temporary_file


def test_dump_empty():
    """Return data mapping from empty config"""
    import nomenclator.config

    config = nomenclator.config.Config(
        descriptions=("comp", "precomp", "roto", "cleanup"),
        create_subfolders=False,
        comp_templates=tuple(),
        project_templates=tuple(),
        max_locations=5,
        max_padding=5,
        username="john-doe",
        username_is_default=True
    )

    data = nomenclator.config.dump(config)
    assert data == collections.OrderedDict()


def test_dump_descriptions():
    """Return data mapping with updated 'descriptions'."""
    import nomenclator.config

    config = nomenclator.config.Config(
        descriptions=("test1", "test2", "test3"),
        create_subfolders=False,
        comp_templates=tuple(),
        project_templates=tuple(),
        max_locations=5,
        max_padding=5,
        username="john-doe",
        username_is_default=True
    )

    data = nomenclator.config.dump(config)
    assert data == collections.OrderedDict([
        ("descriptions", ("test1", "test2", "test3"))
    ])


def test_dump_create_subfolders():
    """Return data mapping with updated 'create-subfolders'."""
    import nomenclator.config

    config = nomenclator.config.Config(
        descriptions=("comp", "precomp", "roto", "cleanup"),
        create_subfolders=True,
        comp_templates=tuple(),
        project_templates=tuple(),
        max_locations=5,
        max_padding=5,
        username="john-doe",
        username_is_default=True
    )

    data = nomenclator.config.dump(config)
    assert data == collections.OrderedDict([
        ("create-subfolders", True)
    ])


def test_dump_max_locations():
    """Return data mapping with updated 'max-locations'."""
    import nomenclator.config

    config = nomenclator.config.Config(
        descriptions=("comp", "precomp", "roto", "cleanup"),
        create_subfolders=False,
        comp_templates=tuple(),
        project_templates=tuple(),
        max_locations=10,
        max_padding=5,
        username="john-doe",
        username_is_default=True
    )

    data = nomenclator.config.dump(config)
    assert data == collections.OrderedDict([("max-locations", 10)])


def test_dump_max_padding():
    """Return data mapping with updated 'max-padding'."""
    import nomenclator.config

    config = nomenclator.config.Config(
        descriptions=("comp", "precomp", "roto", "cleanup"),
        create_subfolders=False,
        comp_templates=tuple(),
        project_templates=tuple(),
        max_locations=5,
        max_padding=3,
        username="john-doe",
        username_is_default=True
    )

    data = nomenclator.config.dump(config)
    assert data == collections.OrderedDict([("max-padding", 3)])


def test_dump_username():
    """Return data mapping with updated 'username'."""
    import nomenclator.config

    config = nomenclator.config.Config(
        descriptions=("comp", "precomp", "roto", "cleanup"),
        create_subfolders=False,
        comp_templates=tuple(),
        project_templates=tuple(),
        max_locations=5,
        max_padding=5,
        username="john-doe",
        username_is_default=False
    )

    data = nomenclator.config.dump(config)
    assert data == collections.OrderedDict([("username", "john-doe")])


def test_dump_comp_templates():
    """Return data mapping with updated 'comp-templates'."""
    import nomenclator.config

    config = nomenclator.config.Config(
        descriptions=("comp", "precomp", "roto", "cleanup"),
        create_subfolders=False,
        comp_templates=(
            nomenclator.config.CompTemplate(
                id="Episodic",
                path="/path/{project}/{episode}/{shot}/scripts",
                base_name="{episode}_{shot}_{description}_v{version}",
                outputs=(
                    nomenclator.config.Template(
                        id="Comp",
                        path="/path/{project}/{episode}/{shot}/comps",
                        base_name="{episode}_{shot}_comp_v{version}",
                    ),
                    nomenclator.config.Template(
                        id="Precomp",
                        path="/path/{project}/{episode}/{shot}/precomps",
                        base_name="{episode}_{shot}_precomp_v{version}",
                    ),
                )
            ),
            nomenclator.config.CompTemplate(
                id="Element",
                path="/path/{project}/build/{element}/scripts",
                base_name="{element}_{description}_v{version}",
                outputs=(
                    nomenclator.config.Template(
                        id="Comp",
                        path="/path/{project}/build/{element}/comps",
                        base_name="{element}_comp_v{version}",
                    ),
                    nomenclator.config.Template(
                        id="Precomp",
                        path="/path/{project}/build/{element}/precomps",
                        base_name="{element}_precomp_v{version}",
                    ),
                )
            ),
        ),
        project_templates=tuple(),
        max_locations=5,
        max_padding=5,
        username="john-doe",
        username_is_default=True
    )

    data = nomenclator.config.dump(config)
    assert data == collections.OrderedDict([
        (
            "comp-templates", (
                collections.OrderedDict([
                    ("id", "Episodic"),
                    ("path", "/path/{project}/{episode}/{shot}/scripts"),
                    ("base-name", "{episode}_{shot}_{description}_v{version}"),
                    (
                        "outputs", (
                            collections.OrderedDict([
                                ("id", "Comp"),
                                ("path", "/path/{project}/{episode}/{shot}/comps"),
                                ("base-name", "{episode}_{shot}_comp_v{version}"),
                            ]),
                            collections.OrderedDict([
                                ("id", "Precomp"),
                                ("path", "/path/{project}/{episode}/{shot}/precomps"),
                                ("base-name", "{episode}_{shot}_precomp_v{version}"),
                            ])
                        )
                    )
                ]),
                collections.OrderedDict([
                    ("id", "Element"),
                    ("path", "/path/{project}/build/{element}/scripts"),
                    ("base-name", "{element}_{description}_v{version}"),
                    (
                        "outputs", (
                            collections.OrderedDict([
                                ("id", "Comp"),
                                ("path", "/path/{project}/build/{element}/comps"),
                                ("base-name", "{element}_comp_v{version}"),
                            ]),
                            collections.OrderedDict([
                                ("id", "Precomp"),
                                ("path", "/path/{project}/build/{element}/precomps"),
                                ("base-name", "{element}_precomp_v{version}"),
                            ])
                        )
                    )
                ])
            )
        )
    ])


def test_dump_project_templates():
    """Return data mapping with updated 'project-templates'."""
    import nomenclator.config

    config = nomenclator.config.Config(
        descriptions=("comp", "precomp", "roto", "cleanup"),
        create_subfolders=False,
        comp_templates=tuple(),
        project_templates=(
            nomenclator.config.Template(
                id="Episodic",
                path="/path/{project}/{episode}/{shot}/scripts",
                base_name="{episode}_{shot}_{description}_v{version}",
            ),
            nomenclator.config.Template(
                id="Element",
                path="/path/{project}/build/{element}/scripts",
                base_name="{element}_{description}_v{version}",
            ),
        ),
        max_locations=5,
        max_padding=5,
        username="john-doe",
        username_is_default=True
    )

    data = nomenclator.config.dump(config)
    assert data == collections.OrderedDict([
        (
            "project-templates", (
                collections.OrderedDict([
                    ("id", "Episodic"),
                    ("path", "/path/{project}/{episode}/{shot}/scripts"),
                    ("base-name", "{episode}_{shot}_{description}_v{version}"),
                ]),
                collections.OrderedDict([
                    ("id", "Element"),
                    ("path", "/path/{project}/build/{element}/scripts"),
                    ("base-name", "{element}_{description}_v{version}"),
                ])
            )
        )
    ])


@pytest.mark.usefixtures("mock_getuser")
def test_load_empty():
    """Return config object from empty data mapping"""
    import nomenclator.config

    config = nomenclator.config.load({})

    assert config == nomenclator.config.Config(
        descriptions=("comp", "precomp", "roto", "cleanup"),
        create_subfolders=False,
        comp_templates=tuple(),
        project_templates=tuple(),
        max_locations=5,
        max_padding=5,
        username="john-doe",
        username_is_default=True
    )


@pytest.mark.usefixtures("mock_getuser")
def test_load_descriptions():
    """Return config with updated 'descriptions'."""
    import nomenclator.config

    config = nomenclator.config.load({
        "descriptions": ("test1", "test2", "test3")
    })

    assert config == nomenclator.config.Config(
        descriptions=("test1", "test2", "test3"),
        create_subfolders=False,
        comp_templates=tuple(),
        project_templates=tuple(),
        max_locations=5,
        max_padding=5,
        username="john-doe",
        username_is_default=True
    )


@pytest.mark.usefixtures("mock_getuser")
def test_load_create_subfolders():
    """Return config with updated 'create-subfolders'."""
    import nomenclator.config

    config = nomenclator.config.load({
        "create-subfolders": True
    })

    assert config == nomenclator.config.Config(
        descriptions=("comp", "precomp", "roto", "cleanup"),
        create_subfolders=True,
        comp_templates=tuple(),
        project_templates=tuple(),
        max_locations=5,
        max_padding=5,
        username="john-doe",
        username_is_default=True
    )


@pytest.mark.usefixtures("mock_getuser")
def test_load_max_locations():
    """Return config with updated 'max-locations'."""
    import nomenclator.config

    config = nomenclator.config.load({
        "max-locations": 10
    })

    assert config == nomenclator.config.Config(
        descriptions=("comp", "precomp", "roto", "cleanup"),
        create_subfolders=False,
        comp_templates=tuple(),
        project_templates=tuple(),
        max_locations=10,
        max_padding=5,
        username="john-doe",
        username_is_default=True
    )


@pytest.mark.usefixtures("mock_getuser")
def test_load_max_padding():
    """Return config with updated 'max-padding'."""
    import nomenclator.config

    config = nomenclator.config.load({
        "max-padding": 3
    })

    assert config == nomenclator.config.Config(
        descriptions=("comp", "precomp", "roto", "cleanup"),
        create_subfolders=False,
        comp_templates=tuple(),
        project_templates=tuple(),
        max_locations=5,
        max_padding=3,
        username="john-doe",
        username_is_default=True
    )


@pytest.mark.usefixtures("mock_getuser")
def test_load_username():
    """Return config with updated 'username'."""
    import nomenclator.config

    config = nomenclator.config.load({
        "username": "steve"
    })

    assert config == nomenclator.config.Config(
        descriptions=("comp", "precomp", "roto", "cleanup"),
        create_subfolders=False,
        comp_templates=tuple(),
        project_templates=tuple(),
        max_locations=5,
        max_padding=5,
        username="steve",
        username_is_default=False
    )


@pytest.mark.usefixtures("mock_getuser")
def test_load_comp_templates():
    """Return config with updated 'comp-templates'."""
    import nomenclator.config

    config = nomenclator.config.load({
        "comp-templates": [
            {
                "id": "Episodic",
                "path": "/path/{project}/{episode}/{shot}/scripts",
                "base-name": "{episode}_{shot}_{description}_v{version}",
                "outputs": [
                    {
                        "id": "Comp",
                        "path": "/path/{project}/{episode}/{shot}/comps",
                        "base-name": "{episode}_{shot}_comp_v{version}",
                    },
                    {
                        "id": "Precomp",
                        "path": "/path/{project}/{episode}/{shot}/precomps",
                        "base-name": "{episode}_{shot}_precomp_v{version}",
                    }
                ]
            },
            {
                "id": "Element",
                "path": "/path/{project}/build/{element}/scripts",
                "base-name": "{element}_{description}_v{version}",
                "outputs": [
                    {
                        "id": "Comp",
                        "path": "/path/{project}/build/{element}/comps",
                        "base-name": "{element}_comp_v{version}",
                    },
                    {
                        "id": "Precomp",
                        "path": "/path/{project}/build/{element}/precomps",
                        "base-name": "{element}_precomp_v{version}",
                    }
                ]
            }
        ]
    })

    assert config == nomenclator.config.Config(
        descriptions=("comp", "precomp", "roto", "cleanup"),
        create_subfolders=False,
        comp_templates=(
            nomenclator.config.CompTemplate(
                id="Episodic",
                path="/path/{project}/{episode}/{shot}/scripts",
                base_name="{episode}_{shot}_{description}_v{version}",
                outputs=(
                    nomenclator.config.Template(
                        id="Comp",
                        path="/path/{project}/{episode}/{shot}/comps",
                        base_name="{episode}_{shot}_comp_v{version}",
                    ),
                    nomenclator.config.Template(
                        id="Precomp",
                        path="/path/{project}/{episode}/{shot}/precomps",
                        base_name="{episode}_{shot}_precomp_v{version}",
                    ),
                )
            ),
            nomenclator.config.CompTemplate(
                id="Element",
                path="/path/{project}/build/{element}/scripts",
                base_name="{element}_{description}_v{version}",
                outputs=(
                    nomenclator.config.Template(
                        id="Comp",
                        path="/path/{project}/build/{element}/comps",
                        base_name="{element}_comp_v{version}",
                    ),
                    nomenclator.config.Template(
                        id="Precomp",
                        path="/path/{project}/build/{element}/precomps",
                        base_name="{element}_precomp_v{version}",
                    ),
                )
            ),
        ),
        project_templates=tuple(),
        max_locations=5,
        max_padding=5,
        username="john-doe",
        username_is_default=True
    )


@pytest.mark.usefixtures("mock_getuser")
def test_load_project_templates():
    """Return config with updated 'project-templates'."""
    import nomenclator.config

    config = nomenclator.config.load({
        "project-templates": [
            {
                "id": "Episodic",
                "path": "/path/{project}/{episode}/{shot}/scripts",
                "base-name": "{episode}_{shot}_{description}_v{version}",
            },
            {
                "id": "Element",
                "path": "/path/{project}/build/{element}/scripts",
                "base-name": "{element}_{description}_v{version}",
            }
        ]
    })

    assert config == nomenclator.config.Config(
        descriptions=("comp", "precomp", "roto", "cleanup"),
        create_subfolders=False,
        comp_templates=tuple(),
        project_templates=(
            nomenclator.config.Template(
                id="Episodic",
                path="/path/{project}/{episode}/{shot}/scripts",
                base_name="{episode}_{shot}_{description}_v{version}",
            ),
            nomenclator.config.Template(
                id="Element",
                path="/path/{project}/build/{element}/scripts",
                base_name="{element}_{description}_v{version}",
            ),
        ),
        max_locations=5,
        max_padding=5,
        username="john-doe",
        username_is_default=True
    )