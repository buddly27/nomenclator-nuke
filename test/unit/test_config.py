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
def mocked_load_template_configs(mocker, temporary_directory):
    """Return mocked 'nomenclator.config.load_template_configs' function."""
    import nomenclator.config
    return mocker.patch.object(nomenclator.config, "load_template_configs")


@pytest.fixture()
def mocked_load_output_template_configs(mocker, temporary_directory):
    """Return mocked 'nomenclator.config.load_output_template_configs' function."""
    import nomenclator.config
    return mocker.patch.object(nomenclator.config, "load_output_template_configs")


@pytest.fixture()
def mocked_dump(mocker, temporary_directory):
    """Return mocked 'nomenclator.config.dump' function."""
    import nomenclator.config
    return mocker.patch.object(nomenclator.config, "dump")


@pytest.fixture()
def mocked_dump_template_configs(mocker, temporary_directory):
    """Return mocked 'nomenclator.config.dump_template_configs' function."""
    import nomenclator.config
    return mocker.patch.object(nomenclator.config, "dump_template_configs")


@pytest.fixture()
def mocked_dump_output_template_configs(mocker, temporary_directory):
    """Return mocked 'nomenclator.config.dump_output_template_configs' function."""
    import nomenclator.config
    return mocker.patch.object(nomenclator.config, "dump_output_template_configs")


def test_path(mocked_expanduser, monkeypatch):
    """Return path to configuration file."""
    monkeypatch.delenv("NOMENCLATOR_CONFIG_PATH", raising=False)

    import nomenclator.config

    path = nomenclator.config.path()
    assert path == os.path.join("__HOME__", ".nuke", "nomenclator.toml")

    mocked_expanduser.assert_called_once_with("~")


def test_path_from_env(mocked_expanduser, monkeypatch):
    """Return path to configuration file fetch from environment"""
    monkeypatch.setenv("NOMENCLATOR_CONFIG_PATH", "__CONFIG__")

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
        comp_template_configs=tuple(),
        project_template_configs=tuple(),
        colorspace_aliases=(("linear", "lin"), ("sRGB", "srgb")),
        tokens=tuple(),
        max_locations=5,
        max_padding=5,
        default_padding=None,
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
        comp_template_configs=tuple(),
        project_template_configs=tuple(),
        colorspace_aliases=(("linear", "lin"), ("sRGB", "srgb")),
        tokens=tuple(),
        max_locations=5,
        max_padding=5,
        default_padding=None,
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
        comp_template_configs=tuple(),
        project_template_configs=tuple(),
        colorspace_aliases=(("linear", "lin"), ("sRGB", "srgb")),
        tokens=tuple(),
        max_locations=5,
        max_padding=5,
        default_padding=None,
        username="john-doe",
        username_is_default=True
    )

    data = nomenclator.config.dump(config)
    assert data == collections.OrderedDict([
        ("create-subfolders", True)
    ])


def test_dump_colorspace_aliases():
    """Return data mapping with updated 'colorspace-aliases'."""
    import nomenclator.config

    config = nomenclator.config.Config(
        descriptions=("comp", "precomp", "roto", "cleanup"),
        create_subfolders=False,
        comp_template_configs=tuple(),
        project_template_configs=tuple(),
        colorspace_aliases=(("color1", "alias1"), ("color2", "alias2")),
        tokens=tuple(),
        max_locations=5,
        max_padding=5,
        default_padding=None,
        username="john-doe",
        username_is_default=True
    )

    data = nomenclator.config.dump(config)
    assert data == collections.OrderedDict([
        ("colorspace-aliases", collections.OrderedDict([
            ("color1", "alias1"), ("color2", "alias2")
        ]))
    ])


def test_dump_tokens():
    """Return data mapping with updated 'tokens'."""
    import nomenclator.config

    config = nomenclator.config.Config(
        descriptions=("comp", "precomp", "roto", "cleanup"),
        create_subfolders=False,
        comp_template_configs=tuple(),
        project_template_configs=tuple(),
        colorspace_aliases=(("linear", "lin"), ("sRGB", "srgb")),
        tokens=(("token1", "value1"), ("token2", "value2")),
        max_locations=5,
        max_padding=5,
        default_padding=None,
        username="john-doe",
        username_is_default=True
    )

    data = nomenclator.config.dump(config)
    assert data == collections.OrderedDict([
        ("tokens", collections.OrderedDict([
            ("token1", "value1"), ("token2", "value2")
        ]))
    ])


def test_dump_max_locations():
    """Return data mapping with updated 'max-locations'."""
    import nomenclator.config

    config = nomenclator.config.Config(
        descriptions=("comp", "precomp", "roto", "cleanup"),
        create_subfolders=False,
        comp_template_configs=tuple(),
        project_template_configs=tuple(),
        colorspace_aliases=(("linear", "lin"), ("sRGB", "srgb")),
        tokens=tuple(),
        max_locations=10,
        max_padding=5,
        default_padding=None,
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
        comp_template_configs=tuple(),
        project_template_configs=tuple(),
        colorspace_aliases=(("linear", "lin"), ("sRGB", "srgb")),
        tokens=tuple(),
        max_locations=5,
        max_padding=3,
        default_padding=None,
        username="john-doe",
        username_is_default=True
    )

    data = nomenclator.config.dump(config)
    assert data == collections.OrderedDict([("max-padding", 3)])


def test_dump_default_padding():
    """Return data mapping with updated 'default-padding'."""
    import nomenclator.config

    config = nomenclator.config.Config(
        descriptions=("comp", "precomp", "roto", "cleanup"),
        create_subfolders=False,
        comp_template_configs=tuple(),
        project_template_configs=tuple(),
        colorspace_aliases=(("linear", "lin"), ("sRGB", "srgb")),
        tokens=tuple(),
        max_locations=5,
        max_padding=5,
        default_padding="###",
        username="john-doe",
        username_is_default=True
    )

    data = nomenclator.config.dump(config)
    assert data == collections.OrderedDict([
        ("default-padding", "###")
    ])


def test_dump_username():
    """Return data mapping with updated 'username'."""
    import nomenclator.config

    config = nomenclator.config.Config(
        descriptions=("comp", "precomp", "roto", "cleanup"),
        create_subfolders=False,
        comp_template_configs=tuple(),
        project_template_configs=tuple(),
        colorspace_aliases=(("linear", "lin"), ("sRGB", "srgb")),
        tokens=tuple(),
        max_locations=5,
        max_padding=5,
        default_padding=None,
        username="john-doe",
        username_is_default=False
    )

    data = nomenclator.config.dump(config)
    assert data == collections.OrderedDict([("username", "john-doe")])


def test_dump_comp_templates(mocked_dump_template_configs):
    """Return data mapping with updated 'comp-templates'."""
    import nomenclator.config

    config = nomenclator.config.Config(
        descriptions=("comp", "precomp", "roto", "cleanup"),
        create_subfolders=False,
        comp_template_configs=("__TEMPLATE1__", "__TEMPLATE2__"),
        project_template_configs=tuple(),
        colorspace_aliases=(("linear", "lin"), ("sRGB", "srgb")),
        tokens=tuple(),
        max_locations=5,
        max_padding=5,
        default_padding=None,
        username="john-doe",
        username_is_default=True
    )

    data = nomenclator.config.dump(config)
    assert data == collections.OrderedDict([
        ("comp-templates", mocked_dump_template_configs.return_value)
    ])

    mocked_dump_template_configs.assert_called_once_with(
        ("__TEMPLATE1__", "__TEMPLATE2__"), include_outputs=True
    )


def test_dump_project_templates(mocked_dump_template_configs):
    """Return data mapping with updated 'project-templates'."""
    import nomenclator.config

    config = nomenclator.config.Config(
        descriptions=("comp", "precomp", "roto", "cleanup"),
        create_subfolders=False,
        comp_template_configs=tuple(),
        project_template_configs=("__TEMPLATE1__", "__TEMPLATE2__"),
        colorspace_aliases=(("linear", "lin"), ("sRGB", "srgb")),
        tokens=tuple(),
        max_locations=5,
        max_padding=5,
        default_padding=None,
        username="john-doe",
        username_is_default=True
    )

    data = nomenclator.config.dump(config)
    assert data == collections.OrderedDict([
        ("project-templates", mocked_dump_template_configs.return_value)
    ])

    mocked_dump_template_configs.assert_called_once_with(
        ("__TEMPLATE1__", "__TEMPLATE2__")
    )


def test_dump_template_configs_empty(mocked_dump_output_template_configs):
    """Return empty list of data mapping for template configs."""
    import nomenclator.config

    data = nomenclator.config.dump_template_configs([])
    assert data == []

    mocked_dump_output_template_configs.assert_not_called()


def test_dump_template_configs(mocked_dump_output_template_configs):
    """Return list of data mapping for template configs."""
    import nomenclator.config

    configs = (
        nomenclator.config.TemplateConfig(
            id="Episodic",
            pattern_path="/path/{project}/{episode}/{shot}/scripts",
            pattern_base="{episode}_{shot}_{description}_v{version}",
            default_expression=r"[\w_.-]+",
            match_start=True,
            match_end=False,
            append_username_to_name=True,
            description="",
            outputs=("__TEMPLATE11__", "__TEMPLATE12__")
        ),
        nomenclator.config.TemplateConfig(
            id="Element",
            pattern_path="/path/{project}/build/{element}/scripts",
            pattern_base="{element}_{description}_v{version}",
            default_expression=r"\w+",
            match_start=False,
            match_end=True,
            append_username_to_name=False,
            description="comp",
            outputs=("__TEMPLATE21__", "__TEMPLATE22__")
        ),
    )

    data = nomenclator.config.dump_template_configs(configs)
    assert data == [
        collections.OrderedDict([
            ("id", "Episodic"),
            ("pattern-path", "/path/{project}/{episode}/{shot}/scripts"),
            ("pattern-base", "{episode}_{shot}_{description}_v{version}"),
            ("match-end", False),
            ("append-username-to-name", True)
        ]),
        collections.OrderedDict([
            ("id", "Element"),
            ("pattern-path", "/path/{project}/build/{element}/scripts"),
            ("pattern-base", "{element}_{description}_v{version}"),
            ("default-expression", r"\w+"),
            ("match-start", False),
            ("description", "comp")
        ]),
    ]

    mocked_dump_output_template_configs.assert_not_called()


def test_dump_template_configs_with_outputs(mocked_dump_output_template_configs):
    """Return list of data mapping for template configs with outputs included."""
    import nomenclator.config

    configs = (
        nomenclator.config.TemplateConfig(
            id="Episodic",
            pattern_path="/path/{project}/{episode}/{shot}/scripts",
            pattern_base="{episode}_{shot}_{description}_v{version}",
            default_expression=r"[\w_.-]+",
            match_start=True,
            match_end=False,
            append_username_to_name=True,
            description="",
            outputs=("__TEMPLATE11__", "__TEMPLATE12__")
        ),
        nomenclator.config.TemplateConfig(
            id="Element",
            pattern_path="/path/{project}/build/{element}/scripts",
            pattern_base="{element}_{description}_v{version}",
            default_expression=r"\w+",
            match_start=False,
            match_end=True,
            append_username_to_name=False,
            description="comp",
            outputs=("__TEMPLATE21__", "__TEMPLATE22__")
        ),
    )

    data = nomenclator.config.dump_template_configs(
        configs, include_outputs=True
    )
    assert data == [
        collections.OrderedDict([
            ("id", "Episodic"),
            ("pattern-path", "/path/{project}/{episode}/{shot}/scripts"),
            ("pattern-base", "{episode}_{shot}_{description}_v{version}"),
            ("match-end", False),
            ("append-username-to-name", True),
            ("outputs", mocked_dump_output_template_configs.return_value)
        ]),
        collections.OrderedDict([
            ("id", "Element"),
            ("pattern-path", "/path/{project}/build/{element}/scripts"),
            ("pattern-base", "{element}_{description}_v{version}"),
            ("default-expression", r"\w+"),
            ("match-start", False),
            ("description", "comp"),
            ("outputs", mocked_dump_output_template_configs.return_value)
        ]),
    ]

    assert mocked_dump_output_template_configs.call_count == 2
    mocked_dump_output_template_configs.assert_any_call(
        ("__TEMPLATE11__", "__TEMPLATE12__")
    )
    mocked_dump_output_template_configs.assert_any_call(
        ("__TEMPLATE21__", "__TEMPLATE22__")
    )


def test_dump_output_template_configs_empty():
    """Return empty list of data mapping for template configs."""
    import nomenclator.config

    data = nomenclator.config.dump_output_template_configs([])
    assert data == []


def test_dump_output_template_configs():
    """Return list of data mapping for template configs."""
    import nomenclator.config

    configs = [
        nomenclator.config.OutputTemplateConfig(
            id="Comp",
            pattern_path="/path/{project}/{episode}/{shot}/comps",
            pattern_base="{episode}_{shot}_comp_v{version}",
            append_username_to_name=False,
            append_colorspace_to_name=True,
            append_passname_to_name=False,
            append_passname_to_subfolder=True,
        ),
        nomenclator.config.OutputTemplateConfig(
            id="Precomp",
            pattern_path="/path/{project}/{episode}/{shot}/precomps",
            pattern_base="{episode}_{shot}_precomp_v{version}",
            append_username_to_name=True,
            append_colorspace_to_name=False,
            append_passname_to_name=True,
            append_passname_to_subfolder=False,
        ),
    ]

    data = nomenclator.config.dump_output_template_configs(configs)
    assert data == [
        collections.OrderedDict([
            ("id", "Comp"),
            ("pattern-path", "/path/{project}/{episode}/{shot}/comps"),
            ("pattern-base", "{episode}_{shot}_comp_v{version}"),
            ("append-colorspace-to-name", True),
            ("append-passname-to-subfolder", True),
        ]),
        collections.OrderedDict([
            ("id", "Precomp"),
            ("pattern-path", "/path/{project}/{episode}/{shot}/precomps"),
            ("pattern-base", "{episode}_{shot}_precomp_v{version}"),
            ("append-username-to-name", True),
            ("append-passname-to-name", True),
        ]),
    ]


@pytest.mark.usefixtures("mock_getuser")
def test_load_empty():
    """Return config object from empty data mapping"""
    import nomenclator.config

    config = nomenclator.config.load({})

    assert config == nomenclator.config.Config(
        descriptions=("comp", "precomp", "roto", "cleanup"),
        create_subfolders=False,
        comp_template_configs=tuple(),
        project_template_configs=tuple(),
        colorspace_aliases=(("linear", "lin"), ("sRGB", "srgb")),
        tokens=tuple(),
        max_locations=5,
        max_padding=5,
        default_padding=None,
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
        comp_template_configs=tuple(),
        project_template_configs=tuple(),
        colorspace_aliases=(("linear", "lin"), ("sRGB", "srgb")),
        tokens=tuple(),
        max_locations=5,
        max_padding=5,
        default_padding=None,
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
        comp_template_configs=tuple(),
        project_template_configs=tuple(),
        colorspace_aliases=(("linear", "lin"), ("sRGB", "srgb")),
        tokens=tuple(),
        max_locations=5,
        max_padding=5,
        default_padding=None,
        username="john-doe",
        username_is_default=True
    )


@pytest.mark.usefixtures("mock_getuser")
def test_load_colorspace_aliases():
    """Return config with updated 'colorspace-aliases'."""
    import nomenclator.config

    config = nomenclator.config.load({
        "colorspace-aliases": {
            "color1": "alias1",
            "color2": "alias2",
        }
    })

    assert config == nomenclator.config.Config(
        descriptions=("comp", "precomp", "roto", "cleanup"),
        create_subfolders=False,
        comp_template_configs=tuple(),
        project_template_configs=tuple(),
        colorspace_aliases=(("color1", "alias1"), ("color2", "alias2")),
        tokens=tuple(),
        max_locations=5,
        max_padding=5,
        default_padding=None,
        username="john-doe",
        username_is_default=True
    )


@pytest.mark.usefixtures("mock_getuser")
def test_load_tokens():
    """Return config with updated 'tokens'."""
    import nomenclator.config

    config = nomenclator.config.load({
        "tokens": {
            "token1": "value1",
            "token2": "value2",
        }
    })

    assert config == nomenclator.config.Config(
        descriptions=("comp", "precomp", "roto", "cleanup"),
        create_subfolders=False,
        comp_template_configs=tuple(),
        project_template_configs=tuple(),
        colorspace_aliases=(("linear", "lin"), ("sRGB", "srgb")),
        tokens=(("token1", "value1"), ("token2", "value2")),
        max_locations=5,
        max_padding=5,
        default_padding=None,
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
        comp_template_configs=tuple(),
        project_template_configs=tuple(),
        colorspace_aliases=(("linear", "lin"), ("sRGB", "srgb")),
        tokens=tuple(),
        max_locations=10,
        max_padding=5,
        default_padding=None,
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
        comp_template_configs=tuple(),
        project_template_configs=tuple(),
        colorspace_aliases=(("linear", "lin"), ("sRGB", "srgb")),
        tokens=tuple(),
        max_locations=5,
        max_padding=3,
        default_padding=None,
        username="john-doe",
        username_is_default=True
    )


@pytest.mark.usefixtures("mock_getuser")
def test_load_default_padding():
    """Return config with updated 'default-padding'."""
    import nomenclator.config

    config = nomenclator.config.load({
        "default-padding": "###"
    })

    assert config == nomenclator.config.Config(
        descriptions=("comp", "precomp", "roto", "cleanup"),
        create_subfolders=False,
        comp_template_configs=tuple(),
        project_template_configs=tuple(),
        colorspace_aliases=(("linear", "lin"), ("sRGB", "srgb")),
        tokens=tuple(),
        max_locations=5,
        max_padding=5,
        default_padding="###",
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
        comp_template_configs=tuple(),
        project_template_configs=tuple(),
        colorspace_aliases=(("linear", "lin"), ("sRGB", "srgb")),
        tokens=tuple(),
        max_locations=5,
        max_padding=5,
        default_padding=None,
        username="steve",
        username_is_default=False
    )


@pytest.mark.usefixtures("mock_getuser")
def test_load_comp_templates(mocked_load_template_configs):
    """Return config with updated 'comp-templates'."""
    import nomenclator.config

    config = nomenclator.config.load({
        "comp-templates": ("__TEMPLATE1__", "__TEMPLATE2__")
    })

    assert config == nomenclator.config.Config(
        descriptions=("comp", "precomp", "roto", "cleanup"),
        create_subfolders=False,
        comp_template_configs=mocked_load_template_configs.return_value,
        project_template_configs=mocked_load_template_configs.return_value,
        colorspace_aliases=(("linear", "lin"), ("sRGB", "srgb")),
        tokens=tuple(),
        max_locations=5,
        max_padding=5,
        default_padding=None,
        username="john-doe",
        username_is_default=True
    )

    assert mocked_load_template_configs.call_count == 2
    mocked_load_template_configs.assert_any_call(
        ("__TEMPLATE1__", "__TEMPLATE2__"), include_outputs=True
    )
    mocked_load_template_configs.assert_any_call([])


@pytest.mark.usefixtures("mock_getuser")
def test_load_project_templates(mocked_load_template_configs):
    """Return config with updated 'project-templates'."""
    import nomenclator.config

    config = nomenclator.config.load({
        "project-templates": ("__TEMPLATE1__", "__TEMPLATE2__")
    })

    assert config == nomenclator.config.Config(
        descriptions=("comp", "precomp", "roto", "cleanup"),
        create_subfolders=False,
        comp_template_configs=mocked_load_template_configs.return_value,
        project_template_configs=mocked_load_template_configs.return_value,
        colorspace_aliases=(("linear", "lin"), ("sRGB", "srgb")),
        tokens=tuple(),
        max_locations=5,
        max_padding=5,
        default_padding=None,
        username="john-doe",
        username_is_default=True
    )

    assert mocked_load_template_configs.call_count == 2
    mocked_load_template_configs.assert_any_call([], include_outputs=True)
    mocked_load_template_configs.assert_any_call(
        ("__TEMPLATE1__", "__TEMPLATE2__")
    )


def test_load_template_configs_empty(mocked_load_output_template_configs):
    """Return empty list of configs for template configs."""
    import nomenclator.config

    data = nomenclator.config.load_template_configs([])
    assert data == tuple()

    mocked_load_output_template_configs.assert_not_called()


def test_load_template_configs_empty_items(mocked_load_output_template_configs):
    """Return list of configs for empty template configs."""
    import nomenclator.config

    configs = [
        {"id": "Episodic"},
        {"id": "Element"}
    ]

    data = nomenclator.config.load_template_configs(configs)
    assert data == (
        nomenclator.config.TemplateConfig(
            id="Episodic",
            pattern_path="",
            pattern_base="",
            default_expression=r"[\w_.-]+",
            match_start=True,
            match_end=True,
            append_username_to_name=False,
            description="",
            outputs=None
        ),
        nomenclator.config.TemplateConfig(
            id="Element",
            pattern_path="",
            pattern_base="",
            default_expression=r"[\w_.-]+",
            match_start=True,
            match_end=True,
            append_username_to_name=False,
            description="",
            outputs=None
        )
    )

    mocked_load_output_template_configs.assert_not_called()


def test_load_template_configs(mocked_load_output_template_configs):
    """Return list of configs for template configs."""
    import nomenclator.config

    configs = [
        {
            "id": "Episodic",
            "pattern-path": "/path/{project}/{episode}/{shot}/scripts",
            "pattern-base": "{episode}_{shot}_{description}_v{version}",
            "default-expression": r"\w+",
            "match-end": False,
            "append-username-to-name": True,
            "outputs": ("__TEMPLATE1__", "__TEMPLATE2__")
        },
        {
            "id": "Element",
            "pattern-path": "/path/{project}/build/{element}/scripts",
            "pattern-base": "{element}_{description}_v{version}",
            "description": "comp",
            "match-start": False,
        }
    ]

    data = nomenclator.config.load_template_configs(configs)
    assert data == (
        nomenclator.config.TemplateConfig(
            id="Episodic",
            pattern_path="/path/{project}/{episode}/{shot}/scripts",
            pattern_base="{episode}_{shot}_{description}_v{version}",
            default_expression=r"\w+",
            match_start=True,
            match_end=False,
            append_username_to_name=True,
            description="",
            outputs=None
        ),
        nomenclator.config.TemplateConfig(
            id="Element",
            pattern_path="/path/{project}/build/{element}/scripts",
            pattern_base="{element}_{description}_v{version}",
            default_expression=r"[\w_.-]+",
            match_start=False,
            match_end=True,
            append_username_to_name=False,
            description="comp",
            outputs=None
        )
    )

    mocked_load_output_template_configs.assert_not_called()


def test_load_template_configs_with_outputs(mocked_load_output_template_configs):
    """Return list of configs for template configs with outputs included."""
    import nomenclator.config

    configs = [
        {
            "id": "Episodic",
            "pattern-path": "/path/{project}/{episode}/{shot}/scripts",
            "pattern-base": "{episode}_{shot}_{description}_v{version}",
            "default-expression": r"\w+",
            "match-end": False,
            "append-username-to-name": True,
            "outputs": ("__TEMPLATE1__", "__TEMPLATE2__")
        },
        {
            "id": "Element",
            "pattern-path": "/path/{project}/build/{element}/scripts",
            "pattern-base": "{element}_{description}_v{version}",
            "description": "comp",
            "match-start": False,
        }
    ]

    data = nomenclator.config.load_template_configs(
        configs, include_outputs=True
    )
    assert data == (
        nomenclator.config.TemplateConfig(
            id="Episodic",
            pattern_path="/path/{project}/{episode}/{shot}/scripts",
            pattern_base="{episode}_{shot}_{description}_v{version}",
            default_expression=r"\w+",
            match_start=True,
            match_end=False,
            append_username_to_name=True,
            description="",
            outputs=mocked_load_output_template_configs.return_value
        ),
        nomenclator.config.TemplateConfig(
            id="Element",
            pattern_path="/path/{project}/build/{element}/scripts",
            pattern_base="{element}_{description}_v{version}",
            default_expression=r"[\w_.-]+",
            match_start=False,
            match_end=True,
            append_username_to_name=False,
            description="comp",
            outputs=mocked_load_output_template_configs.return_value
        )
    )

    assert mocked_load_output_template_configs.call_count == 2
    mocked_load_output_template_configs.assert_any_call(
        ("__TEMPLATE1__", "__TEMPLATE2__")
    )
    mocked_load_output_template_configs.assert_any_call([])


def test_load_output_template_configs_empty():
    """Return empty list of configs for output template configs."""
    import nomenclator.config

    data = nomenclator.config.load_output_template_configs([])
    assert data == tuple()


def test_load_output_template_configs_empty_items():
    """Return list of configs for empty output template configs."""
    import nomenclator.config

    configs = [
        {"id": "Comp"},
        {"id": "Precomp"},
    ]

    data = nomenclator.config.load_output_template_configs(configs)
    assert data == (
        nomenclator.config.OutputTemplateConfig(
            id="Comp",
            pattern_path="",
            pattern_base="",
            append_username_to_name=False,
            append_colorspace_to_name=False,
            append_passname_to_name=False,
            append_passname_to_subfolder=False,
        ),
        nomenclator.config.OutputTemplateConfig(
            id="Precomp",
            pattern_path="",
            pattern_base="",
            append_username_to_name=False,
            append_colorspace_to_name=False,
            append_passname_to_name=False,
            append_passname_to_subfolder=False,
        ),
    )


def test_load_output_template_configs():
    """Return list of configs for output template configs."""
    import nomenclator.config

    configs = [
        {
            "id": "Comp",
            "pattern-path": "/path/{project}/{episode}/{shot}/comps",
            "pattern-base": "{episode}_{shot}_comp_v{version}",
            "append-colorspace-to-name": True,
            "append-passname-to-subfolder": True,
        },
        {
            "id": "Precomp",
            "pattern-path": "/path/{project}/{episode}/{shot}/precomps",
            "pattern-base": "{episode}_{shot}_precomp_v{version}",
            "append-username-to-name": True,
            "append-passname-to-name": True,
        }
    ]

    data = nomenclator.config.load_output_template_configs(configs)
    assert data == (
        nomenclator.config.OutputTemplateConfig(
            id="Comp",
            pattern_path="/path/{project}/{episode}/{shot}/comps",
            pattern_base="{episode}_{shot}_comp_v{version}",
            append_username_to_name=False,
            append_colorspace_to_name=True,
            append_passname_to_name=False,
            append_passname_to_subfolder=True,
        ),
        nomenclator.config.OutputTemplateConfig(
            id="Precomp",
            pattern_path="/path/{project}/{episode}/{shot}/precomps",
            pattern_base="{episode}_{shot}_precomp_v{version}",
            append_username_to_name=True,
            append_colorspace_to_name=False,
            append_passname_to_name=True,
            append_passname_to_subfolder=False,
        ),
    )
