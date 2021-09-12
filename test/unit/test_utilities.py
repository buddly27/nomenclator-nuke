# -*- coding: utf-8 -*-

import os

import pytest


@pytest.fixture()
def mocked_listdir(mocker):
    """Return mocked 'os.listdir' function."""
    return mocker.patch.object(os, "listdir")


@pytest.fixture()
def mocked_isfile(mocker):
    """Return mocked 'os.path.isfile' function."""
    return mocker.patch.object(os.path, "isfile")


@pytest.fixture()
def mocked_resolve(mocker):
    """Return mocked 'nomenclator.template.resolve' function."""
    import nomenclator.template
    return mocker.patch.object(nomenclator.template, "resolve")


@pytest.fixture()
def mocked_fetch_resolved_tokens(mocker):
    """Return mocked 'nomenclator.template.fetch_resolved_tokens' function."""
    import nomenclator.template
    return mocker.patch.object(nomenclator.template, "fetch_resolved_tokens")


def test_fetch_next_version(
    mocked_listdir, mocked_resolve, mocked_fetch_resolved_tokens
):
    """Fetch next version from scene files."""
    import nomenclator.utilities

    mocked_listdir.return_value = [
        "project1.nk",
        "project2_sh003_comp_v001.nk",
        "project2_sh003_comp_v002_steve.nk",
    ]

    mocked_fetch_resolved_tokens.side_effect = [
        None,
        {"version": "001"},
        {"version": "002"},
    ]

    token_mapping = {"key": "value"}
    version = nomenclator.utilities.fetch_next_version(
        "/path", "__PATTERN__", token_mapping
    )

    assert version == 3

    # Ensure that initial token mapping is not mutated.
    assert token_mapping == {"key": "value"}

    mocked_listdir.assert_called_once_with("/path")
    mocked_resolve.assert_called_once_with(
        "__PATTERN__", {"key": "value", "version": r"{version:\d+}"}
    )

    assert mocked_fetch_resolved_tokens.call_count == 3
    mocked_fetch_resolved_tokens.assert_any_call(
        "project1.nk",
        mocked_resolve.return_value,
        match_start=True, match_end=False
    )
    mocked_fetch_resolved_tokens.assert_any_call(
        "project2_sh003_comp_v001.nk",
        mocked_resolve.return_value,
        match_start=True, match_end=False
    )
    mocked_fetch_resolved_tokens.assert_any_call(
        "project2_sh003_comp_v002_steve.nk",
        mocked_resolve.return_value,
        match_start=True, match_end=False
    )


def test_fetch_next_version_empty(
    mocked_listdir, mocked_resolve, mocked_fetch_resolved_tokens
):
    """Fetch version 1 if no scene files in path."""
    import nomenclator.utilities

    mocked_listdir.return_value = []
    token_mapping = {"key": "value"}
    version = nomenclator.utilities.fetch_next_version(
        "/path", "__PATTERN__", token_mapping
    )
    assert version == 1

    # Ensure that initial token mapping is not mutated.
    assert token_mapping == {"key": "value"}

    mocked_listdir.assert_called_once_with("/path")
    mocked_resolve.assert_called_once_with(
        "__PATTERN__", {"key": "value", "version": r"{version:\d+}"}
    )
    mocked_fetch_resolved_tokens.assert_not_called()


def test_fetch_template_config_empty(mocked_fetch_resolved_tokens):
    """Fail to return template config when config list is empty."""
    import nomenclator.utilities

    config = nomenclator.utilities.fetch_template_config("/path", [], {})
    assert config is None

    mocked_fetch_resolved_tokens.assert_not_called()


def test_fetch_template_config_unmatched(mocker, mocked_fetch_resolved_tokens):
    """Fail to return template config when config list do not matched."""
    import nomenclator.utilities

    mocked_fetch_resolved_tokens.return_value = None

    token_mapping = {}
    template_configs = [mocker.Mock(), mocker.Mock(), mocker.Mock()]
    config = nomenclator.utilities.fetch_template_config(
        "/path", template_configs, token_mapping
    )
    assert config is None
    assert token_mapping == {}

    assert mocked_fetch_resolved_tokens.call_count == 3
    for index in range(3):
        mocked_fetch_resolved_tokens.assert_any_call(
            "/path", template_configs[index].pattern_path,
            default_expression=template_configs[index].default_expression,
            match_start=template_configs[index].match_start,
            match_end=template_configs[index].match_end,
        )


def test_fetch_template_config(mocker, mocked_fetch_resolved_tokens):
    """Return matching template config."""
    import nomenclator.utilities

    mocked_fetch_resolved_tokens.side_effect = [None, None, {"key": "value"}]

    token_mapping = {}
    template_configs = [mocker.Mock(), mocker.Mock(), mocker.Mock()]
    config = nomenclator.utilities.fetch_template_config(
        "/path", template_configs, token_mapping
    )
    assert config == template_configs[2]
    assert token_mapping == {"key": "value"}

    assert mocked_fetch_resolved_tokens.call_count == 3
    for index in range(3):
        mocked_fetch_resolved_tokens.assert_any_call(
            "/path", template_configs[index].pattern_path,
            default_expression=template_configs[index].default_expression,
            match_start=template_configs[index].match_start,
            match_end=template_configs[index].match_end,
        )


def test_fetch_output_template_config_empty(mocked_fetch_resolved_tokens):
    """Fail to return output template config when config list is empty."""
    import nomenclator.utilities

    config = nomenclator.utilities.fetch_output_template_config("/path", [])
    assert config is None

    mocked_fetch_resolved_tokens.assert_not_called()


def test_fetch_output_template_config_unmatched(mocker, mocked_fetch_resolved_tokens):
    """Fail to return output template config when config list do not matched."""
    import nomenclator.utilities

    mocked_fetch_resolved_tokens.return_value = None

    template_configs = [
        mocker.Mock(pattern_base="__BASE__"),
        mocker.Mock(pattern_base="__BASE__"),
        mocker.Mock(pattern_base="__BASE__"),
    ]
    config = nomenclator.utilities.fetch_output_template_config(
        "/path", template_configs
    )
    assert config is None

    assert mocked_fetch_resolved_tokens.call_count == 3
    for index in range(3):
        mocked_fetch_resolved_tokens.assert_any_call(
            "/path", template_configs[index].pattern_path,
            default_expression=r"[\w_.-]+",
            match_start=True,
            match_end=True,
        )


def test_fetch_output_template_config(mocker, mocked_fetch_resolved_tokens):
    """Return matching output template config."""
    import nomenclator.utilities

    mocked_fetch_resolved_tokens.side_effect = [None, None, {"key": "value"}]

    template_configs = [
        mocker.Mock(pattern_base="__BASE__"),
        mocker.Mock(pattern_base="__BASE__"),
        mocker.Mock(pattern_base="__BASE__"),
    ]
    config = nomenclator.utilities.fetch_output_template_config(
        "/path", template_configs
    )
    assert config == template_configs[2]

    assert mocked_fetch_resolved_tokens.call_count == 3
    for index in range(3):
        mocked_fetch_resolved_tokens.assert_any_call(
            "/path", template_configs[index].pattern_path,
            default_expression=r"[\w_.-]+",
            match_start=True,
            match_end=True,
        )


def test_fetch_nodes(mocker):
    """Return tuple with output nodes and all node names."""
    import nuke
    import nomenclator.utilities

    mocked_nodes = [
        mocker.Mock(**{
            "Class.return_value": "Write",
            "name.return_value": "Output1",
        }),
        mocker.Mock(**{
            "Class.return_value": "Write",
            "name.return_value": "Output2",
        }),
        mocker.Mock(**{
            "Class.return_value": "DeepWrite",
            "name.return_value": "Output3",
        }),
        mocker.Mock(**{
            "Class.return_value": "Other",
            "name.return_value": "Node",
        }),
    ]

    nuke.allNodes.return_value = mocked_nodes

    nodes, node_names = nomenclator.utilities.fetch_nodes()

    assert nodes == mocked_nodes[:-1]
    assert node_names == ["Output1", "Output2", "Output3", "Node"]


def test_fetch_recent_comp_paths():
    """Return list of comp path recently used."""
    import nuke
    import nomenclator.utilities

    nuke.recentFile.side_effect = [
        "/path1/comp11.nk",
        "/path1/comp12.nk",
        "/path2/comp21.nk",
        "/path3/comp31.nk",
        "/path3/comp32.nk",
        "/path4/comp41.nk",
        RuntimeError("no recent file has been found")
    ]

    paths = nomenclator.utilities.fetch_recent_comp_paths()
    assert paths == ("/path1", "/path2", "/path3", "/path4")

    assert nuke.recentFile.call_count == 7
    nuke.recentFile.assert_any_call(1)
    nuke.recentFile.assert_any_call(2)
    nuke.recentFile.assert_any_call(3)
    nuke.recentFile.assert_any_call(4)
    nuke.recentFile.assert_any_call(5)
    nuke.recentFile.assert_any_call(6)
    nuke.recentFile.assert_any_call(7)


def test_fetch_recent_comp_paths_with_max_value():
    """Return a maximum number of list of comp paths recently used."""
    import nuke
    import nomenclator.utilities

    nuke.recentFile.side_effect = [
        "/path1/comp11.nk",
        "/path1/comp12.nk",
        "/path2/comp21.nk",
        "/path3/comp31.nk",
        "/path3/comp32.nk",
        "/path4/comp41.nk",
        RuntimeError("no recent file has been found")
    ]

    paths = nomenclator.utilities.fetch_recent_comp_paths(max_values=3)
    assert paths == ("/path1", "/path2")

    assert nuke.recentFile.call_count == 3
    nuke.recentFile.assert_any_call(1)
    nuke.recentFile.assert_any_call(2)
    nuke.recentFile.assert_any_call(3)


def test_fetch_recent_project_paths(mocker, mocked_isfile):
    """Return list of project path recently used."""
    import hiero.ui
    import nomenclator.utilities

    items = [
        mocker.Mock(**{"text.return_value": "/path1/project11.hrox"}),
        mocker.Mock(**{"text.return_value": "/path1/project12.hrox"}),
        mocker.Mock(**{"text.return_value": "/path2/project21.hrox"}),
        mocker.Mock(**{"text.return_value": "/path3/project31.hrox"}),
        mocker.Mock(**{"text.return_value": "/path3/project32.hrox"}),
        mocker.Mock(**{"text.return_value": "/path4/project41.hrox"}),
        mocker.Mock(**{"text.return_value": "1"}),
        mocker.Mock(**{"text.return_value": "2"}),
    ]

    mocked_action = hiero.ui.findMenuAction.return_value
    mocked_action_menu = mocked_action.menu.return_value
    mocked_action_menu.actions.return_value = items
    mocked_isfile.side_effect = [True, True, True, True, True, True, False, False]

    paths = nomenclator.utilities.fetch_recent_project_paths()
    assert paths == ("/path1", "/path2", "/path3", "/path4")

    hiero.ui.findMenuAction.assert_called_once_with("foundry.project.recentprojects")
    mocked_action.menu.assert_called_once()
    mocked_action_menu.actions.assert_called_once()

    assert mocked_isfile.call_count == 8
    mocked_isfile.assert_any_call("/path1/project11.hrox")
    mocked_isfile.assert_any_call("/path1/project12.hrox")
    mocked_isfile.assert_any_call("/path2/project21.hrox")
    mocked_isfile.assert_any_call("/path3/project31.hrox")
    mocked_isfile.assert_any_call("/path3/project32.hrox")
    mocked_isfile.assert_any_call("/path4/project41.hrox")
    mocked_isfile.assert_any_call("1")
    mocked_isfile.assert_any_call("2")


def test_fetch_recent_project_paths_with_max_value(mocker, mocked_isfile):
    """Return a maximum number of list of project paths recently used."""
    import hiero.ui
    import nomenclator.utilities

    items = [
        mocker.Mock(**{"text.return_value": "/path1/project11.hrox"}),
        mocker.Mock(**{"text.return_value": "/path1/project12.hrox"}),
        mocker.Mock(**{"text.return_value": "/path2/project21.hrox"}),
        mocker.Mock(**{"text.return_value": "/path3/project31.hrox"}),
        mocker.Mock(**{"text.return_value": "/path3/project32.hrox"}),
        mocker.Mock(**{"text.return_value": "/path4/project41.hrox"}),
        mocker.Mock(**{"text.return_value": "1"}),
        mocker.Mock(**{"text.return_value": "2"}),
    ]

    mocked_action = hiero.ui.findMenuAction.return_value
    mocked_action_menu = mocked_action.menu.return_value
    mocked_action_menu.actions.return_value = items
    mocked_isfile.side_effect = [True, True, True]

    paths = nomenclator.utilities.fetch_recent_project_paths(max_values=3)
    assert paths == ("/path1", "/path2")

    hiero.ui.findMenuAction.assert_called_once_with("foundry.project.recentprojects")
    mocked_action.menu.assert_called_once()
    mocked_action_menu.actions.assert_called_once()

    assert mocked_isfile.call_count == 3
    mocked_isfile.assert_any_call("/path1/project11.hrox")
    mocked_isfile.assert_any_call("/path1/project12.hrox")
    mocked_isfile.assert_any_call("/path2/project21.hrox")


def test_fetch_recent_project_paths_error_action(mocked_isfile):
    """Fail to return list of project paths recently used if action is None."""
    import hiero.ui
    import nomenclator.utilities

    hiero.ui.findMenuAction.return_value = None

    paths = nomenclator.utilities.fetch_recent_project_paths()
    assert paths == tuple()

    hiero.ui.findMenuAction.assert_called_once_with("foundry.project.recentprojects")
    mocked_isfile.assert_not_called()


def test_fetch_recent_project_paths_error_action_menu(mocked_isfile):
    """Fail to return list of project paths recently used if action menu is None."""
    import hiero.ui
    import nomenclator.utilities

    mocked_action = hiero.ui.findMenuAction.return_value
    mocked_action.menu.return_value = None

    paths = nomenclator.utilities.fetch_recent_project_paths()
    assert paths == tuple()

    hiero.ui.findMenuAction.assert_called_once_with("foundry.project.recentprojects")
    mocked_action.menu.assert_called_once()
    mocked_isfile.assert_not_called()


def test_fetch_paddings_hashes_notation(mocker):
    """Return paddings in hashes notation."""
    import nuke
    import nomenclator.utilities

    mocked_knob = mocker.Mock(**{"value.return_value": "Hashes (#)"})
    nuke.toNode.return_value = {"UISequenceDisplayMode": mocked_knob}

    paddings = nomenclator.utilities.fetch_paddings()
    assert paddings == ("#", "##", "###", "####", "#####")

    nuke.toNode.assert_called_once_with("preferences")
    mocked_knob.value.assert_called_once()


def test_fetch_paddings_hashes_notation_with_max_value(mocker):
    """Return maximum number of paddings in hashes notation."""
    import nuke
    import nomenclator.utilities

    mocked_knob = mocker.Mock(**{"value.return_value": "Hashes (#)"})
    nuke.toNode.return_value = {"UISequenceDisplayMode": mocked_knob}

    paddings = nomenclator.utilities.fetch_paddings(max_value=3)
    assert paddings == ("#", "##", "###")

    nuke.toNode.assert_called_once_with("preferences")
    mocked_knob.value.assert_called_once()


def test_fetch_paddings_printf_notation(mocker):
    """Return paddings in printf notation."""
    import nuke
    import nomenclator.utilities

    mocked_knob = mocker.Mock(**{"value.return_value": "Printf Notation (%d)"})
    nuke.toNode.return_value = {"UISequenceDisplayMode": mocked_knob}

    paddings = nomenclator.utilities.fetch_paddings()
    assert paddings == ("%01d", "%02d", "%03d", "%04d", "%05d")

    nuke.toNode.assert_called_once_with("preferences")
    mocked_knob.value.assert_called_once()


def test_fetch_paddings_printf_notation_with_max_value(mocker):
    """Return maximum number of paddings in printf notation."""
    import nuke
    import nomenclator.utilities

    mocked_knob = mocker.Mock(**{"value.return_value": "Printf Notation (%d)"})
    nuke.toNode.return_value = {"UISequenceDisplayMode": mocked_knob}

    paddings = nomenclator.utilities.fetch_paddings(max_value=3)
    assert paddings == ("%01d", "%02d", "%03d")

    nuke.toNode.assert_called_once_with("preferences")
    mocked_knob.value.assert_called_once()


def test_fetch_paddings_default_preferences_error():
    """Return default paddings when preferences node is None."""
    import nuke
    import nomenclator.utilities

    nuke.toNode.return_value = None

    paddings = nomenclator.utilities.fetch_paddings()
    assert paddings == ("#", "##", "###", "####", "#####")

    nuke.toNode.assert_called_once_with("preferences")


def test_fetch_paddings_default_preferences_knob_error(mocker):
    """Return default paddings when preferences knob does not exist."""
    import nuke
    import nomenclator.utilities

    nuke.toNode.return_value = mocker.MagicMock(**{
        "__getitem__.side_effect": NameError(
            "knob UISequenceDisplayMode does not exist"
        )
    })

    paddings = nomenclator.utilities.fetch_paddings()
    assert paddings == ("#", "##", "###", "####", "#####")

    nuke.toNode.assert_called_once_with("preferences")


def test_fetch_paddings_default_preferences_knob_value_error(mocker):
    """Return default paddings when preferences knob return unexpected value."""
    import nuke
    import nomenclator.utilities

    mocked_knob = mocker.Mock(**{"value.return_value": "Unexpected"})
    nuke.toNode.return_value = {"UISequenceDisplayMode": mocked_knob}

    paddings = nomenclator.utilities.fetch_paddings()
    assert paddings == ("#", "##", "###", "####", "#####")

    nuke.toNode.assert_called_once_with("preferences")
    mocked_knob.value.assert_called_once()


def test_fetch_current_comp_path():
    """Return current composition path."""
    import nuke
    import nomenclator.utilities

    path = nomenclator.utilities.fetch_current_comp_path()
    assert path == nuke.scriptName.return_value


def test_fetch_current_comp_path_error():
    """Fail to return current composition path."""
    import nuke
    import nomenclator.utilities

    nuke.scriptName.side_effect = RuntimeError("no filename available, have you saved?")

    path = nomenclator.utilities.fetch_current_comp_path()
    assert path == ""


def test_fetch_current_project_path(mocker):
    """Return current project path."""
    import hiero.core
    import nomenclator.utilities

    projects = [mocker.Mock(), mocker.Mock(), mocker.Mock()]
    hiero.core.projects.return_value = projects

    path = nomenclator.utilities.fetch_current_project_path()
    assert path == projects[2].path.return_value


def test_fetch_current_project_path_empty():
    """Fail to current project path when project list is empty."""
    import hiero.core
    import nomenclator.utilities

    hiero.core.projects.return_value = []

    path = nomenclator.utilities.fetch_current_project_path()
    assert path == ""


def test_fetch_output_path(mocker):
    """Fetch output path from node."""
    import nomenclator.utilities

    knob = mocker.Mock()
    knob_mapping = {"file": knob}
    node = mocker.MagicMock(__getitem__=lambda _, key: knob_mapping[key])

    path = nomenclator.utilities.fetch_output_path(node)
    assert path == knob.value.return_value


def test_fetch_colorspace(mocker):
    """Fetch colorspace from node."""
    import nomenclator.utilities

    knob = mocker.Mock()
    knob_mapping = {"colorspace": knob}
    node = mocker.MagicMock(knob=lambda key: knob_mapping.get(key))

    value = nomenclator.utilities.fetch_colorspace(node, {})
    assert value == knob.value.return_value


def test_fetch_colorspace_default(mocker):
    """Fetch default colorspace value from node when knob does not exist."""
    import nomenclator.utilities

    knob_mapping = {}
    node = mocker.MagicMock(knob=lambda key: knob_mapping.get(key))

    value = nomenclator.utilities.fetch_colorspace(node, {})
    assert value == "none"


def test_fetch_colorspace_alias(mocker):
    """Fetch colorspace from node with alias."""
    import nomenclator.utilities

    knob = mocker.Mock(**{"value.return_value": "sRGB"})
    knob_mapping = {"colorspace": knob}
    node = mocker.MagicMock(knob=lambda key: knob_mapping.get(key))

    value = nomenclator.utilities.fetch_colorspace(node, {"sRGB": "srgb"})
    assert value == "srgb"


def test_fetch_file_type(mocker):
    """Return file type from node."""
    import nomenclator.utilities

    knob = mocker.Mock(**{"value.return_value": " exr "})
    knob_mapping = {"file_type": knob}
    node = mocker.MagicMock(__getitem__=lambda _, key: knob_mapping[key])

    value = nomenclator.utilities.fetch_file_type(node, "__DEFAULT__")
    assert value == "exr"


def test_fetch_file_type_default(mocker):
    """Return default file type from node."""
    import nomenclator.utilities

    knob = mocker.Mock(**{"value.return_value": "  "})
    knob_mapping = {"file_type": knob}
    node = mocker.MagicMock(__getitem__=lambda _, key: knob_mapping[key])

    value = nomenclator.utilities.fetch_file_type(node, "__DEFAULT__")
    assert value == "__DEFAULT__"


def test_fetch_file_types(mocker):
    """Return file types from node."""
    import nomenclator.utilities

    knob = mocker.Mock(**{"values.return_value": ["", "exr", "dpx", "mov\t\t\tffmpeg"]})
    knob_mapping = {"file_type": knob}
    node = mocker.MagicMock(__getitem__=lambda _, key: knob_mapping[key])

    values = nomenclator.utilities.fetch_file_types(node)
    assert values == ("exr", "dpx", "mov")


def test_has_multiple_views_true(mocker):
    """Indicate that a node is configured with multiple views."""
    import nomenclator.utilities

    knob = mocker.Mock(**{"value.return_value": "left right"})
    knob_mapping = {"views": knob}
    node = mocker.MagicMock(__getitem__=lambda _, key: knob_mapping[key])

    assert nomenclator.utilities.has_multiple_views(node) is True


def test_has_multiple_views_false(mocker):
    """Indicate that a node is not configured with multiple views."""
    import nomenclator.utilities

    knob = mocker.Mock(**{"value.return_value": "main"})
    knob_mapping = {"views": knob}
    node = mocker.MagicMock(__getitem__=lambda _, key: knob_mapping[key])

    assert nomenclator.utilities.has_multiple_views(node) is False


def test_is_enabled_true(mocker):
    """Indicate that a node is enabled."""
    import nomenclator.utilities

    knob = mocker.Mock(**{"value.return_value": False})
    knob_mapping = {"disable": knob}
    node = mocker.MagicMock(__getitem__=lambda _, key: knob_mapping[key])

    assert nomenclator.utilities.is_enabled(node) is True


def test_is_enabled_false(mocker):
    """Indicate that a node is not enabled."""
    import nomenclator.utilities

    knob = mocker.Mock(**{"value.return_value": True})
    knob_mapping = {"disable": knob}
    node = mocker.MagicMock(__getitem__=lambda _, key: knob_mapping[key])

    assert nomenclator.utilities.is_enabled(node) is False
