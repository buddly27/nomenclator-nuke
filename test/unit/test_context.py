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
def mocked_fetch_output_template_config(mocker):
    """Return mocked 'nomenclator.utilities.fetch_output_template_config' function."""
    import nomenclator.utilities
    return mocker.patch.object(nomenclator.utilities, "fetch_output_template_config", )


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
def mocked_fetch_output_path(mocker):
    """Return mocked 'nomenclator.utilities.fetch_output_path' function."""
    import nomenclator.utilities
    return mocker.patch.object(nomenclator.utilities, "fetch_output_path", )


@pytest.fixture()
def mocked_is_enabled(mocker):
    """Return mocked 'nomenclator.utilities.is_enabled' function."""
    import nomenclator.utilities
    return mocker.patch.object(nomenclator.utilities, "is_enabled", )


@pytest.fixture()
def mocked_fetch_file_type(mocker):
    """Return mocked 'nomenclator.utilities.fetch_file_type' function."""
    import nomenclator.utilities
    return mocker.patch.object(nomenclator.utilities, "fetch_file_type", )


@pytest.fixture()
def mocked_fetch_file_types(mocker):
    """Return mocked 'nomenclator.utilities.fetch_file_types' function."""
    import nomenclator.utilities
    return mocker.patch.object(nomenclator.utilities, "fetch_file_types", )


@pytest.fixture()
def mocked_fetch_colorspace(mocker):
    """Return mocked 'nomenclator.utilities.fetch_colorspace' function."""
    import nomenclator.utilities
    return mocker.patch.object(nomenclator.utilities, "fetch_colorspace", )


@pytest.fixture()
def mocked_has_multiple_views(mocker):
    """Return mocked 'nomenclator.utilities.has_multiple_views' function."""
    import nomenclator.utilities
    return mocker.patch.object(nomenclator.utilities, "has_multiple_views", )


@pytest.fixture()
def mocked_fetch_recent_comp_paths(mocker):
    """Return mocked 'nomenclator.utilities.fetch_recent_comp_paths' function."""
    import nomenclator.utilities
    return mocker.patch.object(nomenclator.utilities, "fetch_recent_comp_paths")


@pytest.fixture()
def mocked_fetch_recent_project_paths(mocker):
    """Return mocked 'nomenclator.utilities.fetch_recent_project_paths' function."""
    import nomenclator.utilities
    return mocker.patch.object(nomenclator.utilities, "fetch_recent_project_paths")


@pytest.fixture()
def mocked_fetch_current_comp_path(mocker):
    """Return mocked 'nomenclator.utilities.fetch_current_comp_path' function."""
    import nomenclator.utilities
    return mocker.patch.object(nomenclator.utilities, "fetch_current_comp_path")


@pytest.fixture()
def mocked_fetch_current_project_path(mocker):
    """Return mocked 'nomenclator.utilities.fetch_current_project_path' function."""
    import nomenclator.utilities
    return mocker.patch.object(nomenclator.utilities, "fetch_current_project_path")


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


@pytest.mark.parametrize("options", [
    {},
    {"is_project": False},
], ids=[
    "default",
    "with-options",
])
def test_fetch_comp(
    mocker, mocked_fetch_outputs, mocked_fetch_paddings,
    mocked_fetch_recent_comp_paths, mocked_fetch_recent_project_paths,
    mocked_fetch_current_comp_path, mocked_fetch_current_project_path,
    mocked_fetch_template_config, options
):
    """Return comp context object."""
    import nomenclator.context

    template_config = mocker.Mock()

    config = mocker.Mock()
    mocked_fetch_current_comp_path.return_value = "/path/to/comp.nk"
    mocked_fetch_template_config.return_value = template_config
    context = nomenclator.context.fetch(config, **options)

    assert context == nomenclator.context.Context(
        location_path="/path/to",
        recent_locations=mocked_fetch_recent_comp_paths.return_value,
        path="/path/to/comp.nk",
        suffix="nk",
        version=None,
        description=config.default_description,
        descriptions=config.descriptions,
        append_username_to_name=False,
        padding=config.default_padding,
        paddings=mocked_fetch_paddings.return_value,
        create_subfolders=config.create_subfolders,
        tokens=config.tokens,
        username=config.username,
        template_configs=config.comp_template_configs,
        outputs=mocked_fetch_outputs.return_value,
        error=None,
    )

    mocked_fetch_template_config.assert_called_once_with(
        "/path/to", config.comp_template_configs, {}
    )
    mocked_fetch_outputs.assert_called_once_with(
        config, template_config.outputs
    )
    mocked_fetch_paddings.assert_called_once_with(
        max_value=config.max_padding
    )
    mocked_fetch_recent_comp_paths.assert_called_once_with(
        max_values=config.max_locations
    )
    mocked_fetch_recent_project_paths.assert_not_called()
    mocked_fetch_current_comp_path.assert_called_once()
    mocked_fetch_current_project_path.assert_not_called()


@pytest.mark.parametrize("options", [
    {},
    {"is_project": False},
], ids=[
    "default",
    "with-options",
])
def test_fetch_comp_empty_path(
    mocker, mocked_fetch_outputs, mocked_fetch_paddings,
    mocked_fetch_recent_comp_paths, mocked_fetch_recent_project_paths,
    mocked_fetch_current_comp_path, mocked_fetch_current_project_path,
    mocked_fetch_template_config, options
):
    """Return comp context object when current path is empty."""
    import nomenclator.context

    config = mocker.Mock()
    mocked_fetch_current_comp_path.return_value = ""
    context = nomenclator.context.fetch(config, **options)

    assert context == nomenclator.context.Context(
        location_path="",
        recent_locations=mocked_fetch_recent_comp_paths.return_value,
        path="",
        suffix="nk",
        version=None,
        description=config.default_description,
        descriptions=config.descriptions,
        append_username_to_name=False,
        padding=config.default_padding,
        paddings=mocked_fetch_paddings.return_value,
        create_subfolders=config.create_subfolders,
        tokens=config.tokens,
        username=config.username,
        template_configs=config.comp_template_configs,
        outputs=mocked_fetch_outputs.return_value,
        error=None,
    )

    mocked_fetch_template_config.assert_not_called()
    mocked_fetch_outputs.assert_called_once_with(config, [])
    mocked_fetch_paddings.assert_called_once_with(
        max_value=config.max_padding
    )
    mocked_fetch_recent_comp_paths.assert_called_once_with(
        max_values=config.max_locations
    )
    mocked_fetch_recent_project_paths.assert_not_called()
    mocked_fetch_current_comp_path.assert_called_once()
    mocked_fetch_current_project_path.assert_not_called()


def test_fetch_project(
    mocker, mocked_fetch_outputs, mocked_fetch_paddings,
    mocked_fetch_recent_comp_paths, mocked_fetch_recent_project_paths,
    mocked_fetch_current_comp_path, mocked_fetch_current_project_path,
):
    """Return project context object."""
    import nomenclator.context

    config = mocker.Mock()
    mocked_fetch_current_project_path.return_value = "/path/to/project.hrox"
    context = nomenclator.context.fetch(config, is_project=True)

    assert context == nomenclator.context.Context(
        location_path="/path/to",
        recent_locations=mocked_fetch_recent_project_paths.return_value,
        path="/path/to/project.hrox",
        suffix="hrox",
        version=None,
        description=config.default_description,
        descriptions=config.descriptions,
        append_username_to_name=False,
        padding=config.default_padding,
        paddings=mocked_fetch_paddings.return_value,
        create_subfolders=config.create_subfolders,
        tokens=config.tokens,
        username=config.username,
        template_configs=config.project_template_configs,
        outputs=tuple(),
        error=None,
    )

    mocked_fetch_outputs.assert_not_called()
    mocked_fetch_paddings.assert_called_once_with(
        max_value=config.max_padding
    )
    mocked_fetch_recent_project_paths.assert_called_once_with(
        max_values=config.max_locations
    )
    mocked_fetch_recent_comp_paths.assert_not_called()
    mocked_fetch_current_project_path.assert_called_once()
    mocked_fetch_current_comp_path.assert_not_called()


def test_fetch_project_empty_path(
    mocker, mocked_fetch_outputs, mocked_fetch_paddings,
    mocked_fetch_recent_comp_paths, mocked_fetch_recent_project_paths,
    mocked_fetch_current_comp_path, mocked_fetch_current_project_path,
):
    """Return project context object when current path is empty."""
    import nomenclator.context

    config = mocker.Mock()
    mocked_fetch_current_project_path.return_value = ""
    context = nomenclator.context.fetch(config, is_project=True)

    assert context == nomenclator.context.Context(
        location_path="",
        recent_locations=mocked_fetch_recent_project_paths.return_value,
        path="",
        suffix="hrox",
        version=None,
        description=config.default_description,
        descriptions=config.descriptions,
        append_username_to_name=False,
        padding=config.default_padding,
        paddings=mocked_fetch_paddings.return_value,
        create_subfolders=config.create_subfolders,
        tokens=config.tokens,
        username=config.username,
        template_configs=config.project_template_configs,
        outputs=tuple(),
        error=None,
    )

    mocked_fetch_outputs.assert_not_called()
    mocked_fetch_paddings.assert_called_once_with(
        max_value=config.max_padding
    )
    mocked_fetch_recent_project_paths.assert_called_once_with(
        max_values=config.max_locations
    )
    mocked_fetch_recent_comp_paths.assert_not_called()
    mocked_fetch_current_project_path.assert_called_once()
    mocked_fetch_current_comp_path.assert_not_called()


def test_fetch_outputs_without_templates(
    mocker, mocked_fetch_nodes, mocked_fetch_output_path,
    mocked_fetch_output_template_config, mocked_is_enabled,
    mocked_fetch_file_type, mocked_fetch_file_types, mocked_fetch_colorspace,
    mocked_has_multiple_views,
):
    """Return output context objects with no incoming template configs."""
    import nomenclator.context

    config = mocker.Mock(
        colorspace_aliases=(("sRGB", "srgb"),),
    )

    nodes = [mocker.MagicMock(**{"name.return_value": "node1"})]
    mocked_fetch_output_path.side_effect = ["/path/to/output1.dpx"]
    mocked_fetch_nodes.return_value = (nodes, ["node1", "node2", "node3"])

    contexts = nomenclator.context.fetch_outputs(config, [])

    assert contexts == (
        nomenclator.context.OutputContext(
            name="node1",
            new_name="node1",
            blacklisted_names=("node2", "node3"),
            path="/path/to/output1.dpx",
            passname="node1",
            enabled=mocked_is_enabled.return_value,
            destination="",
            destinations=tuple(),
            file_type=mocked_fetch_file_type.return_value,
            file_types=mocked_fetch_file_types.return_value,
            multi_views=mocked_has_multiple_views.return_value,
            colorspace=mocked_fetch_colorspace.return_value,
            append_username_to_name=False,
            append_colorspace_to_name=False,
            append_passname_to_name=False,
            append_passname_to_subfolder=False,
            error=None,
        ),
    )

    mocked_fetch_nodes.assert_called_once()
    mocked_fetch_output_path.assert_called_once_with(nodes[0])
    mocked_fetch_output_template_config.assert_not_called()
    mocked_is_enabled.assert_called_once_with(nodes[0])
    mocked_fetch_file_type.assert_called_once_with(nodes[0], "exr")
    mocked_fetch_file_types.assert_called_once_with(nodes[0])
    mocked_fetch_colorspace.assert_called_once_with(nodes[0], {"sRGB": "srgb"})
    mocked_has_multiple_views.assert_called_once_with(nodes[0])


def test_fetch_outputs_empty_path(
    mocker, mocked_fetch_nodes, mocked_fetch_output_path,
    mocked_fetch_output_template_config, mocked_is_enabled,
    mocked_fetch_file_type, mocked_fetch_file_types, mocked_fetch_colorspace,
    mocked_has_multiple_views,
):
    """Return output context objects when node path is empty."""
    import nomenclator.context

    config = mocker.Mock(
        colorspace_aliases=(("sRGB", "srgb"),),
    )

    template_configs = (
        mocker.Mock(id="comps"),
        mocker.Mock(id="precomps"),
        mocker.Mock(id="roto"),
    )

    nodes = [mocker.MagicMock(**{"name.return_value": "node1"})]
    mocked_fetch_output_path.side_effect = [""]
    mocked_fetch_nodes.return_value = (nodes, ["node1", "node2", "node3"])

    contexts = nomenclator.context.fetch_outputs(config, template_configs)

    assert contexts == (
        nomenclator.context.OutputContext(
            name="node1",
            new_name="node1",
            blacklisted_names=("node2", "node3"),
            path="",
            passname="node1",
            enabled=mocked_is_enabled.return_value,
            destination="comps",
            destinations=("comps", "precomps", "roto"),
            file_type=mocked_fetch_file_type.return_value,
            file_types=mocked_fetch_file_types.return_value,
            multi_views=mocked_has_multiple_views.return_value,
            colorspace=mocked_fetch_colorspace.return_value,
            append_username_to_name=template_configs[0].append_username_to_name,
            append_colorspace_to_name=template_configs[0].append_colorspace_to_name,
            append_passname_to_name=template_configs[0].append_passname_to_name,
            append_passname_to_subfolder=template_configs[0].append_passname_to_subfolder,
            error=None,
        ),
    )

    mocked_fetch_nodes.assert_called_once()
    mocked_fetch_output_path.assert_called_once_with(nodes[0])
    mocked_fetch_output_template_config.assert_not_called()
    mocked_is_enabled.assert_called_once_with(nodes[0])
    mocked_fetch_file_type.assert_called_once_with(nodes[0], "exr")
    mocked_fetch_file_types.assert_called_once_with(nodes[0])
    mocked_fetch_colorspace.assert_called_once_with(nodes[0], {"sRGB": "srgb"})
    mocked_has_multiple_views.assert_called_once_with(nodes[0])


def test_fetch_outputs(
    mocker, mocked_fetch_nodes, mocked_fetch_output_path,
    mocked_fetch_output_template_config, mocked_is_enabled,
    mocked_fetch_file_type, mocked_fetch_file_types, mocked_fetch_colorspace,
    mocked_has_multiple_views,
):
    """Return output context objects."""
    import nomenclator.context

    config = mocker.Mock(
        colorspace_aliases=(("sRGB", "srgb"),),
    )

    template_configs = (
        mocker.Mock(id="comps"),
        mocker.Mock(id="precomps"),
        mocker.Mock(id="roto"),
    )

    nodes = [mocker.MagicMock(**{"name.return_value": "node1"})]
    mocked_fetch_output_path.side_effect = ["/path/to/output1.dpx"]
    mocked_fetch_nodes.return_value = (nodes, ["node1", "node2", "node3"])
    mocked_fetch_output_template_config.return_value = None

    contexts = nomenclator.context.fetch_outputs(config, template_configs)

    assert contexts == (
        nomenclator.context.OutputContext(
            name="node1",
            new_name="node1",
            blacklisted_names=("node2", "node3"),
            path="/path/to/output1.dpx",
            passname="node1",
            enabled=mocked_is_enabled.return_value,
            destination="comps",
            destinations=("comps", "precomps", "roto"),
            file_type=mocked_fetch_file_type.return_value,
            file_types=mocked_fetch_file_types.return_value,
            multi_views=mocked_has_multiple_views.return_value,
            colorspace=mocked_fetch_colorspace.return_value,
            append_username_to_name=template_configs[0].append_username_to_name,
            append_colorspace_to_name=template_configs[0].append_colorspace_to_name,
            append_passname_to_name=template_configs[0].append_passname_to_name,
            append_passname_to_subfolder=template_configs[0].append_passname_to_subfolder,
            error=None,
        ),
    )

    mocked_fetch_nodes.assert_called_once()
    mocked_fetch_output_path.assert_called_once_with(nodes[0])
    mocked_fetch_output_template_config.assert_called_once_with(
        "/path/to", template_configs
    )
    mocked_is_enabled.assert_called_once_with(nodes[0])
    mocked_fetch_file_type.assert_called_once_with(nodes[0], "exr")
    mocked_fetch_file_types.assert_called_once_with(nodes[0])
    mocked_fetch_colorspace.assert_called_once_with(nodes[0], {"sRGB": "srgb"})
    mocked_has_multiple_views.assert_called_once_with(nodes[0])


def test_fetch_outputs_matching_config(
    mocker, mocked_fetch_nodes, mocked_fetch_output_path,
    mocked_fetch_output_template_config, mocked_is_enabled,
    mocked_fetch_file_type, mocked_fetch_file_types, mocked_fetch_colorspace,
    mocked_has_multiple_views,
):
    """Return output context objects with one matching config."""
    import nomenclator.context

    config = mocker.Mock(
        colorspace_aliases=(("sRGB", "srgb"),),
    )

    template_configs = (
        mocker.Mock(id="comps"),
        mocker.Mock(id="precomps"),
        mocker.Mock(id="roto"),
    )

    nodes = [mocker.MagicMock(**{"name.return_value": "node1"})]
    mocked_fetch_output_path.side_effect = ["/path/to/output1.dpx"]
    mocked_fetch_nodes.return_value = (nodes, ["node1", "node2", "node3"])
    mocked_fetch_output_template_config.return_value = template_configs[2]

    contexts = nomenclator.context.fetch_outputs(config, template_configs)

    assert contexts == (
        nomenclator.context.OutputContext(
            name="node1",
            new_name="node1",
            blacklisted_names=("node2", "node3"),
            path="/path/to/output1.dpx",
            passname="node1",
            enabled=mocked_is_enabled.return_value,
            destination="roto",
            destinations=("comps", "precomps", "roto"),
            file_type=mocked_fetch_file_type.return_value,
            file_types=mocked_fetch_file_types.return_value,
            multi_views=mocked_has_multiple_views.return_value,
            colorspace=mocked_fetch_colorspace.return_value,
            append_username_to_name=template_configs[2].append_username_to_name,
            append_colorspace_to_name=template_configs[2].append_colorspace_to_name,
            append_passname_to_name=template_configs[2].append_passname_to_name,
            append_passname_to_subfolder=template_configs[2].append_passname_to_subfolder,
            error=None,
        ),
    )

    mocked_fetch_nodes.assert_called_once()
    mocked_fetch_output_path.assert_called_once_with(nodes[0])
    mocked_fetch_output_template_config.assert_called_once_with(
        "/path/to", template_configs
    )
    mocked_is_enabled.assert_called_once_with(nodes[0])
    mocked_fetch_file_type.assert_called_once_with(nodes[0], "exr")
    mocked_fetch_file_types.assert_called_once_with(nodes[0])
    mocked_fetch_colorspace.assert_called_once_with(nodes[0], {"sRGB": "srgb"})
    mocked_has_multiple_views.assert_called_once_with(nodes[0])


def test_update_empty(
    mocker, mocked_fetch_next_version, mocked_fetch_template_config,
    mocked_generate_scene_name, mocked_update_outputs
):
    """Return context with empty path."""
    import nomenclator.context

    mocked_fetch_template_config.return_value = None

    context = mocker.Mock(
        tokens=(("key1", "value1"), ("key2", "value2"), ("key3", "value3")),
        template_configs=("__CONFIG1__", "__CONFIG2__"),
        location_path=""
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

    mocked_update_outputs.assert_called_once_with(
        context.outputs, [], {}, ignore_errors=True
    )

    context._replace.assert_called_once_with(
        path="",
        version=None,
        outputs=mocked_update_outputs.return_value,
        error=None
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
        mocked_fetch_template_config.return_value.pattern_base,
        token_mapping
    )

    mocked_generate_scene_name.assert_called_once_with(
        mocked_fetch_template_config.return_value.pattern_base,
        context.suffix,
        append_username=context.append_username_to_name,
        token_mapping=token_mapping
    )

    mocked_update_outputs.assert_called_once_with(
        context.outputs,
        mocked_fetch_template_config.return_value.outputs,
        token_mapping
    )

    context._replace.assert_called_once_with(
        path=os.path.join("__PATH__", "__NAME__"),
        version=mocked_fetch_next_version.return_value,
        outputs=mocked_update_outputs.return_value,
        error=None,
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

    mocked_resolve.side_effect = ["__PATH1__", "__PATH2__", "__PATH3__"]
    mocked_generate_output_name.side_effect = [
        "__NAME1__", "__NAME2__", "__NAME3__"
    ]

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

    assert mocked_resolve.call_count == 3
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
    mocked_resolve.assert_any_call(
        template_configs[0].pattern_path,
        {
            "key": "value",
            "colorspace": contexts[2].colorspace,
            "passname": contexts[2].passname,
        }
    )

    assert mocked_generate_output_name.call_count == 3
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
    mocked_generate_output_name.assert_any_call(
        template_configs[0].pattern_base,
        contexts[2].file_type,
        append_passname_to_subfolder=contexts[2].append_passname_to_subfolder,
        append_passname=contexts[2].append_passname_to_name,
        append_colorspace=contexts[2].append_colorspace_to_name,
        append_username=contexts[2].append_username_to_name,
        multi_views=contexts[2].multi_views,
        token_mapping={
            "key": "value",
            "colorspace": contexts[2].colorspace,
            "passname": contexts[2].passname,
        }
    )

    contexts[0]._replace.assert_called_once_with(
        path=os.path.join("__PATH1__", "__NAME1__"),
        destination="Target1",
        destinations=("Target1", "Target2"),
        error=None
    )
    contexts[1]._replace.assert_called_once_with(
        path=os.path.join("__PATH2__", "__NAME2__"),
        destination="Target2",
        destinations=("Target1", "Target2"),
        error=None
    )
    contexts[2]._replace.assert_called_once_with(
        path=os.path.join("__PATH3__", "__NAME3__"),
        destination="Target1",
        destinations=("Target1", "Target2"),
        error=None
    )


def test_update_outputs_without_templates(mocker, mocked_generate_output_name, mocked_resolve):
    """Return output contexts with no incoming template configs."""
    import nomenclator.context

    mocked_resolve.side_effect = ["__PATH1__", "__PATH2__", "__PATH3__"]
    mocked_generate_output_name.side_effect = [
        "__NAME1__", "__NAME2__", "__NAME3__"
    ]

    contexts = [
        mocker.Mock(destination="Target1"),
        mocker.Mock(destination="Target2"),
        mocker.Mock(destination="Unknown"),
    ]

    token_mapping = {"key": "value"}

    results = nomenclator.context.update_outputs(
        contexts, [], token_mapping
    )
    assert results == (
        contexts[0]._replace.return_value,
        contexts[1]._replace.return_value,
        contexts[2]._replace.return_value,
    )

    mocked_resolve.assert_not_called()
    mocked_generate_output_name.assert_not_called()

    contexts[0]._replace.assert_called_once_with(
        path="",
        destination="",
        destinations=tuple(),
        error={
            "message": "No output template configurations found.",
            "details": (
                "You must set at least one output template "
                "configuration to generate names.\n"
                "Please read the documentation at "
                "http://nomenclator-nuke.readthedocs.io/en/stable/\n"
            )
        }
    )
    contexts[1]._replace.assert_called_once_with(
        path="",
        destination="",
        destinations=tuple(),
        error={
            "message": "No output template configurations found.",
            "details": (
                "You must set at least one output template "
                "configuration to generate names.\n"
                "Please read the documentation at "
                "http://nomenclator-nuke.readthedocs.io/en/stable/\n"
            )
        }
    )
    contexts[2]._replace.assert_called_once_with(
        path="",
        destination="",
        destinations=tuple(),
        error={
            "message": "No output template configurations found.",
            "details": (
                "You must set at least one output template "
                "configuration to generate names.\n"
                "Please read the documentation at "
                "http://nomenclator-nuke.readthedocs.io/en/stable/\n"
            )
        }
    )
