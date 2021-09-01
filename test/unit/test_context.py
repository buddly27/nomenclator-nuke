# -*- coding: utf-8 -*-

import os

import pytest


@pytest.fixture()
def mocked_fetch_next_version(mocker):
    """Return mocked 'nomenclator.utilities.fetch_next_version' function."""
    import nomenclator.utilities
    return mocker.patch.object(nomenclator.utilities, "fetch_next_version", )


@pytest.fixture()
def mocked_fetch_template_config(mocker):
    """Return mocked 'nomenclator.utilities.fetch_template_config' function."""
    import nomenclator.utilities
    return mocker.patch.object(nomenclator.utilities, "fetch_template_config", )


@pytest.fixture()
def mocked_fetch_nodes(mocker):
    """Return mocked 'nomenclator.utilities.fetch_nodes' function."""
    import nomenclator.utilities
    return mocker.patch.object(nomenclator.utilities, "fetch_nodes", )


@pytest.fixture()
def mocked_fetch_paddings(mocker):
    """Return mocked 'nomenclator.utilities.fetch_paddings' function."""
    import nomenclator.utilities
    return mocker.patch.object(nomenclator.utilities, "fetch_paddings")


@pytest.fixture()
def mocked_fetch_recent_comp_paths(mocker):
    """Return mocked 'nomenclator.utilities.fetch_recent_comp_paths' function."""
    import nomenclator.utilities
    return mocker.patch.object(nomenclator.utilities, "fetch_recent_comp_paths")


@pytest.fixture()
def mocked_generate_scene_name(mocker):
    """Return mocked 'nomenclator.template.generate_scene_name' function."""
    import nomenclator.template
    return mocker.patch.object(nomenclator.template, "generate_scene_name")


@pytest.fixture()
def mocked_generate_output_name(mocker):
    """Return mocked 'nomenclator.template.generate_output_name' function."""
    import nomenclator.template
    return mocker.patch.object(nomenclator.template, "generate_output_name")


@pytest.fixture()
def mocked_resolve(mocker):
    """Return mocked 'nomenclator.template.resolve' function."""
    import nomenclator.template
    return mocker.patch.object(nomenclator.template, "resolve")


@pytest.fixture()
def mocked_fetch_outputs(mocker):
    """Return mocked 'nomenclator.context.fetch_outputs' function."""
    import nomenclator.context
    return mocker.patch.object(nomenclator.context, "fetch_outputs")


@pytest.fixture()
def mocked_update_outputs(mocker):
    """Return mocked 'nomenclator.context.update_outputs' function."""
    import nomenclator.context
    return mocker.patch.object(nomenclator.context, "update_outputs")


@pytest.fixture()
def nodes(mocker):
    """Return mocked nodes."""
    knob_mappings = [
        {
            "file": mocker.Mock(**{"value.return_value": ""}),
            "views": mocker.Mock(**{"value.return_value": "main"}),
            "colorspace": mocker.Mock(**{"value.return_value": "sRGB"}),
            "disable": mocker.Mock(**{"value.return_value": False}),
            "file_type": mocker.Mock(**{
                "value.return_value": "",
                "values.return_value": ["exr", "dpx", "tiff", "mov\t\t\tffmpeg"]
            }),
        },
        {
            "file": mocker.Mock(**{"value.return_value": "/path/to/file.dpx"}),
            "views": mocker.Mock(**{"value.return_value": "left right"}),
            "colorspace": mocker.Mock(**{"value.return_value": "rec709"}),
            "disable": mocker.Mock(**{"value.return_value": False}),
            "file_type": mocker.Mock(**{
                "value.return_value": "dpx",
                "values.return_value": ["exr", "dpx", "tiff", "mov\t\t\tffmpeg"],

            }),
        },
        {
            "file": mocker.Mock(**{"value.return_value": ""}),
            "views": mocker.Mock(**{"value.return_value": "main"}),
            "colorspace": mocker.Mock(**{"value.return_value": "linear"}),
            "disable": mocker.Mock(**{"value.return_value": True}),
            "file_type": mocker.Mock(**{
                "value.return_value": "",
                "values.return_value": ["exr", "abc"]
            }),
        }
    ]

    return [
        mocker.MagicMock(
            __getitem__=lambda _, key: knob_mappings[0][key],
            **{"name.return_value": "node1"}
        ),
        mocker.MagicMock(
            __getitem__=lambda _, key: knob_mappings[1][key],
            **{"name.return_value": "node2"}
        ),
        mocker.MagicMock(
            __getitem__=lambda _, key: knob_mappings[2][key],
            **{"name.return_value": "node3"}
        ),
    ]


@pytest.mark.parametrize("options", [
    {},
    {"is_project": False},
], ids=[
    "default",
    "with-options",
])
def test_fetch_comp(
    mocker, mocked_fetch_outputs, mocked_fetch_paddings,
    mocked_fetch_recent_comp_paths, options
):
    """Return comp context object."""
    import nomenclator.context

    mocked_fetch_paddings.return_value = ("#", "##", "###")

    config = mocker.Mock(descriptions=("test1", "test2", "test3"))

    context = nomenclator.context.fetch(config, **options)

    assert context == nomenclator.context.Context(
        location_path="",
        recent_locations=mocked_fetch_recent_comp_paths.return_value,
        path="",
        suffix="nk",
        version=None,
        description="test1",
        descriptions=("test1", "test2", "test3"),
        append_username_to_name=False,
        padding="#",
        paddings=("#", "##", "###"),
        create_subfolders=config.create_subfolders,
        tokens=config.tokens,
        username=config.username,
        template_configs=config.comp_template_configs,
        outputs=mocked_fetch_outputs.return_value
    )

    mocked_fetch_outputs.assert_called_once_with(config)
    mocked_fetch_paddings.assert_called_once_with(
        max_value=config.max_padding
    )
    mocked_fetch_recent_comp_paths.assert_called_once_with(
        max_values=config.max_locations
    )


def test_fetch_project(
    mocker, mocked_fetch_outputs, mocked_fetch_paddings,
    mocked_fetch_recent_comp_paths
):
    """Return project context object."""
    import nomenclator.context

    mocked_fetch_paddings.return_value = ("#", "##", "###")

    config = mocker.Mock(descriptions=("test1", "test2", "test3"))

    context = nomenclator.context.fetch(config, is_project=True)

    assert context == nomenclator.context.Context(
        location_path="",
        recent_locations=mocked_fetch_recent_comp_paths.return_value,
        path="",
        suffix="hrox",
        version=None,
        description="test1",
        descriptions=("test1", "test2", "test3"),
        append_username_to_name=False,
        padding="#",
        paddings=("#", "##", "###"),
        create_subfolders=config.create_subfolders,
        tokens=config.tokens,
        username=config.username,
        template_configs=config.project_template_configs,
        outputs=tuple()
    )

    mocked_fetch_outputs.assert_not_called()
    mocked_fetch_paddings.assert_called_once_with(
        max_value=config.max_padding
    )
    mocked_fetch_recent_comp_paths.assert_called_once_with(
        max_values=config.max_locations
    )


def test_fetch_outputs(mocker, nodes, mocked_fetch_nodes):
    """Return output context objects."""
    import nomenclator.context

    mocked_fetch_nodes.return_value = (
        nodes, ["node1", "node2", "node3", "node4", "node5"]
    )

    config = mocker.Mock(colorspace_aliases=(("sRGB", "srgb"),))

    contexts = nomenclator.context.fetch_outputs(config)

    assert contexts == (
        nomenclator.context.OutputContext(
            name="node1",
            blacklisted_names=("node2", "node3", "node4", "node5"),
            path="",
            passname="node1",
            enabled=True,
            destination="",
            destinations=tuple(),
            file_type="exr",
            file_types=("exr", "dpx", "tiff", "mov"),
            multi_views=False,
            colorspace="srgb",
            append_username_to_name=False,
            append_colorspace_to_name=False,
            append_passname_to_name=False,
            append_passname_to_subfolder=False
        ),
        nomenclator.context.OutputContext(
            name="node2",
            blacklisted_names=("node1", "node3", "node4", "node5"),
            path="/path/to/file.dpx",
            passname="node2",
            enabled=True,
            destination="",
            destinations=tuple(),
            file_type="dpx",
            file_types=("exr", "dpx", "tiff", "mov"),
            multi_views=True,
            colorspace="rec709",
            append_username_to_name=False,
            append_colorspace_to_name=False,
            append_passname_to_name=False,
            append_passname_to_subfolder=False
        ),
        nomenclator.context.OutputContext(
            name="node3",
            blacklisted_names=("node1", "node2", "node4", "node5"),
            path="",
            passname="node3",
            enabled=False,
            destination="",
            destinations=tuple(),
            file_type="exr",
            file_types=("exr", "abc"),
            multi_views=False,
            colorspace="linear",
            append_username_to_name=False,
            append_colorspace_to_name=False,
            append_passname_to_name=False,
            append_passname_to_subfolder=False
        ),
    )


def test_update_empty(
    mocker, mocked_fetch_next_version, mocked_fetch_template_config,
    mocked_generate_scene_name, mocked_update_outputs
):
    """Return context with empty path."""
    import nomenclator.context

    mocked_fetch_template_config.return_value = None

    context = mocker.Mock(
        tokens=(("key1", "value1"), ("key2", "value2"), ("key3", "value3")),
    )

    result = nomenclator.context.update(context)
    assert result == context._replace.return_value

    mocked_fetch_template_config.assert_called_once_with(
        context.location_path,
        context.template_configs,
        {"key1": "value1", "key2": "value2", "key3": "value3"}
    )

    mocked_fetch_next_version.assert_not_called()
    mocked_generate_scene_name.assert_not_called()

    mocked_update_outputs.assert_called_once_with(context, [], {})

    context._replace.assert_called_once_with(
        path="",
        version=None,
        outputs=mocked_update_outputs.return_value
    )


def test_update(
    mocker, mocked_fetch_next_version, mocked_fetch_template_config,
    mocked_generate_scene_name, mocked_update_outputs
):
    """Return context with generated path."""
    import nomenclator.context

    mocked_fetch_next_version.return_value = 3
    mocked_generate_scene_name.return_value = "__NAME__"

    context = mocker.Mock(
        location_path="__PATH__",
        tokens=(("key1", "value1"), ("key2", "value2"), ("key3", "value3")),
    )

    result = nomenclator.context.update(context)
    assert result == context._replace.return_value

    token_mapping = {
        "version": "003",
        "padding": context.padding,
        "description": context.description,
        "username": context.username,
        "key1": "value1",
        "key2": "value2",
        "key3": "value3"
    }

    mocked_fetch_template_config.assert_called_once_with(
        context.location_path,
        context.template_configs,
        token_mapping
    )

    mocked_fetch_next_version.assert_called_once_with(
        context.location_path,
        mocked_fetch_template_config.return_value.pattern_path,
        token_mapping
    )

    mocked_generate_scene_name.assert_called_once_with(
        mocked_fetch_template_config.return_value.pattern_base,
        context.suffix,
        append_username=context.append_username_to_name,
        token_mapping=token_mapping
    )

    mocked_update_outputs.assert_called_once_with(
        context,
        mocked_fetch_template_config.return_value.outputs,
        token_mapping
    )

    context._replace.assert_called_once_with(
        path=os.path.join("__PATH__", "__NAME__"),
        version=mocked_fetch_next_version.return_value,
        outputs=mocked_update_outputs.return_value
    )


def test_update_outputs_empty(mocked_generate_output_name, mocked_resolve):
    """Return empty output contexts."""
    import nomenclator.context

    results = nomenclator.context.update_outputs([], [], {})
    assert results == tuple()

    mocked_generate_output_name.assert_not_called()
    mocked_resolve.assert_not_called()


def test_update_outputs(mocker, mocked_generate_output_name, mocked_resolve):
    """Return output contexts."""
    import nomenclator.context

    mocked_resolve.side_effect = ["__PATH1__", "__PATH2__"]
    mocked_generate_output_name.side_effect = ["__NAME1__", "__NAME2__"]

    contexts = [
        mocker.Mock(destination="Target1"),
        mocker.Mock(destination="Target2"),
        mocker.Mock(destination="Unknown"),
    ]

    template_configs = [
        mocker.Mock(id="Target1"),
        mocker.Mock(id="Target2"),
    ]

    token_mapping = {"key": "value"}

    results = nomenclator.context.update_outputs(
        contexts, template_configs, token_mapping
    )
    assert results == (
        contexts[0]._replace.return_value,
        contexts[1]._replace.return_value,
        contexts[2]._replace.return_value,
    )

    assert mocked_resolve.call_count == 2
    mocked_resolve.assert_any_call(
        template_configs[0].pattern_path,
        {
            "key": "value",
            "colorspace": contexts[0].colorspace,
            "passname": contexts[0].passname,
        }
    )
    mocked_resolve.assert_any_call(
        template_configs[1].pattern_path,
        {
            "key": "value",
            "colorspace": contexts[1].colorspace,
            "passname": contexts[1].passname,
        }
    )

    assert mocked_generate_output_name.call_count == 2
    mocked_generate_output_name.assert_any_call(
        template_configs[0].pattern_base,
        contexts[0].file_type,
        append_passname_to_subfolder=contexts[0].append_passname_to_subfolder,
        append_passname=contexts[0].append_passname_to_name,
        append_colorspace=contexts[0].append_colorspace_to_name,
        append_username=contexts[0].append_username_to_name,
        multi_views=contexts[0].multi_views,
        token_mapping={
            "key": "value",
            "colorspace": contexts[0].colorspace,
            "passname": contexts[0].passname,
        }
    )
    mocked_generate_output_name.assert_any_call(
        template_configs[1].pattern_base,
        contexts[1].file_type,
        append_passname_to_subfolder=contexts[1].append_passname_to_subfolder,
        append_passname=contexts[1].append_passname_to_name,
        append_colorspace=contexts[1].append_colorspace_to_name,
        append_username=contexts[1].append_username_to_name,
        multi_views=contexts[1].multi_views,
        token_mapping={
            "key": "value",
            "colorspace": contexts[1].colorspace,
            "passname": contexts[1].passname,
        }
    )

    contexts[0]._replace.assert_called_once_with(
        path=os.path.join("__PATH1__", "__NAME1__")
    )
    contexts[1]._replace.assert_called_once_with(
        path=os.path.join("__PATH2__", "__NAME2__")
    )
    contexts[2]._replace.assert_called_once_with(path="")
