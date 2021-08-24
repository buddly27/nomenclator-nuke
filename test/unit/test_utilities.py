# -*- coding: utf-8 -*-

import sys

import pytest


@pytest.fixture()
def mocked_fetch_nodes(mocker):
    """Return mocked 'nomenclator.utilities.fetch_nodes' function."""
    import nomenclator.utilities
    return mocker.patch.object(
        nomenclator.utilities, "fetch_nodes",
        return_value=("__NODES__", "__NAMES__")
    )


@pytest.fixture()
def mocked_fetch_paddings(mocker):
    """Return mocked 'nomenclator.utilities.fetch_paddings' function."""
    import nomenclator.utilities
    return mocker.patch.object(nomenclator.utilities, "fetch_paddings")


@pytest.fixture()
def mocked_sanitize_template(mocker):
    """Return mocked 'nomenclator.utilities.sanitize_template' function."""
    import nomenclator.utilities
    return mocker.patch.object(nomenclator.utilities, "sanitize_template")


def test_fetch_output_context(mocker, mocked_fetch_nodes, mocked_fetch_paddings):
    """Return a mapping with all data needed for output management."""
    import nomenclator.utilities

    config = mocker.Mock()
    context = nomenclator.utilities.fetch_output_context(config)

    assert context == {
        "nodes": "__NODES__",
        "node_names": "__NAMES__",
        "paddings": mocked_fetch_paddings.return_value
    }

    mocked_fetch_nodes.assert_called_once()
    mocked_fetch_paddings.assert_called_once_with(
        max_value=config.max_padding
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


def test_fetch_recent_locations():
    """Return list of path recently used."""
    import nuke
    import nomenclator.utilities

    nuke.recentFile.side_effect = [
        "/path1/comp1.nk",
        "/path1/comp1.nk",
        "/path2/comp2.nk",
        "/path3/comp3.nk",
        "/path3/comp3.nk",
        "/path4/comp4.nk",
        RuntimeError("no recent file has been found")
    ]

    paths = nomenclator.utilities.fetch_recent_comp_paths()
    assert paths == ["/path1", "/path2", "/path3", "/path4"]

    assert nuke.recentFile.call_count == 7
    nuke.recentFile.assert_any_call(1)
    nuke.recentFile.assert_any_call(2)
    nuke.recentFile.assert_any_call(3)
    nuke.recentFile.assert_any_call(4)
    nuke.recentFile.assert_any_call(5)
    nuke.recentFile.assert_any_call(6)
    nuke.recentFile.assert_any_call(7)


def test_fetch_recent_locations_with_max_value():
    """Return a maximum number of list of path recently used."""
    import nuke
    import nomenclator.utilities

    nuke.recentFile.side_effect = [
        "/path1/comp1.nk",
        "/path1/comp1.nk",
        "/path2/comp2.nk",
        "/path3/comp3.nk",
        "/path3/comp3.nk",
        "/path4/comp4.nk",
        RuntimeError("no recent file has been found")
    ]

    paths = nomenclator.utilities.fetch_recent_comp_paths(max_values=3)
    assert paths == ["/path1", "/path2"]

    assert nuke.recentFile.call_count == 3
    nuke.recentFile.assert_any_call(1)
    nuke.recentFile.assert_any_call(2)
    nuke.recentFile.assert_any_call(3)


def test_fetch_paddings_hashes_notation(mocker):
    """Return paddings in hashes notation."""
    import nuke
    import nomenclator.utilities

    mocked_knob = mocker.Mock(**{"value.return_value": "Hashes (#)"})
    nuke.toNode.return_value = {"UISequenceDisplayMode": mocked_knob}

    paddings = nomenclator.utilities.fetch_paddings()
    assert paddings == ["#", "##", "###", "####", "#####"]

    nuke.toNode.assert_called_once_with("preferences")
    mocked_knob.value.assert_called_once()


def test_fetch_paddings_hashes_notation_with_max_value(mocker):
    """Return maximum number of paddings in hashes notation."""
    import nuke
    import nomenclator.utilities

    mocked_knob = mocker.Mock(**{"value.return_value": "Hashes (#)"})
    nuke.toNode.return_value = {"UISequenceDisplayMode": mocked_knob}

    paddings = nomenclator.utilities.fetch_paddings(max_value=3)
    assert paddings == ["#", "##", "###"]

    nuke.toNode.assert_called_once_with("preferences")
    mocked_knob.value.assert_called_once()


def test_fetch_paddings_printf_notation(mocker):
    """Return paddings in printf notation."""
    import nuke
    import nomenclator.utilities

    mocked_knob = mocker.Mock(**{"value.return_value": "Printf Notation (%d)"})
    nuke.toNode.return_value = {"UISequenceDisplayMode": mocked_knob}

    paddings = nomenclator.utilities.fetch_paddings()
    assert paddings == ["%01d", "%02d", "%03d", "%04d", "%05d"]

    nuke.toNode.assert_called_once_with("preferences")
    mocked_knob.value.assert_called_once()


def test_fetch_paddings_printf_notation_with_max_value(mocker):
    """Return maximum number of paddings in printf notation."""
    import nuke
    import nomenclator.utilities

    mocked_knob = mocker.Mock(**{"value.return_value": "Printf Notation (%d)"})
    nuke.toNode.return_value = {"UISequenceDisplayMode": mocked_knob}

    paddings = nomenclator.utilities.fetch_paddings(max_value=3)
    assert paddings == ["%01d", "%02d", "%03d"]

    nuke.toNode.assert_called_once_with("preferences")
    mocked_knob.value.assert_called_once()


def test_fetch_paddings_default_preferences_error():
    """Return default paddings when preferences node is None."""
    import nuke
    import nomenclator.utilities

    nuke.toNode.return_value = None

    paddings = nomenclator.utilities.fetch_paddings()
    assert paddings == ["#", "##", "###", "####", "#####"]

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
    assert paddings == ["#", "##", "###", "####", "#####"]

    nuke.toNode.assert_called_once_with("preferences")


def test_fetch_paddings_default_preferences_knob_value_error(mocker):
    """Return default paddings when preferences knob return unexpected value."""
    import nuke
    import nomenclator.utilities

    mocked_knob = mocker.Mock(**{"value.return_value": "Unexpected"})
    nuke.toNode.return_value = {"UISequenceDisplayMode": mocked_knob}

    paddings = nomenclator.utilities.fetch_paddings()
    assert paddings == ["#", "##", "###", "####", "#####"]

    nuke.toNode.assert_called_once_with("preferences")
    mocked_knob.value.assert_called_once()


@pytest.mark.parametrize("template, expected", [
    (
        r"/path/to/location",
        r"/path/to/location",
    ),
    (
        r"/path/{project}/{episode}",
        r"/path/(?P<project>[\w_.\-]+)/(?P<episode>[\w_.\-]+)",
    ),
    (
        r"/path/{project:^J_.*$}/{episode:^ep\d+$}",
        r"/path/(?P<project>^J_.*$)/(?P<episode>^ep\d+$)",
    ),
], ids=[
    "no-tokens",
    "path-with-tokens",
    "path-with-tokens-and-patterns",
])
def test_construct_regexp(mocked_sanitize_template, template, expected):
    """Create corresponding regular expression."""
    mocked_sanitize_template.return_value = template

    import nomenclator.utilities
    assert nomenclator.utilities.construct_regexp(template) == expected


def test_construct_regexp_with_default(mocked_sanitize_template):
    """Create corresponding regular expression with default expression."""
    template = r"/path/{project}/{episode}"
    mocked_sanitize_template.return_value = template

    import nomenclator.utilities
    regexp = nomenclator.utilities.construct_regexp(
        template, default_expression=r"\w+"
    )

    assert regexp == r"/path/(?P<project>\w+)/(?P<episode>\w+)"


@pytest.mark.parametrize("template, expected", [
    (
        r"/^p@th./t0^/l*cation",
        r"/\^p@th\./t0\^/l\*cation",
    ),
    (
        r"/^p@th./{project}/{episode}",
        r"/\^p@th\./{project}/{episode}",
    ),
    (
        r"/^p@th./{project:^J_.*$}/{episode:^ep\d+$}",
        r"/\^p@th\./{project:^J_.*$}/{episode:^ep\d+$}",
    ),
    (
        r"C:\\^p@th.\t0^\l*cation",
        r"C:\\\\\^p@th\.\\t0\^\\l\*cation",
    ),
    (
        r"C:\\^p@th.\{project}\{episode}",
        r"C:\\\\\^p@th\.\\{project}\\{episode}",
    ),
    (
        r"C:\\^p@th.\{project:^J_.*$}\{episode:^ep\d+$}",
        r"C:\\\\\^p@th\.\\{project:^J_.*$}\\{episode:^ep\d+$}",
    ),
], ids=[
    "unix-path-without-tokens",
    "unix-path-with-tokens",
    "unix-path-with-tokens-and-patterns",
    "windows-path-without-tokens",
    "windows-path-with-tokens",
    "windows-path-with-tokens-and-patterns",
])
def test_sanitize_template(template, expected):
    """Sanitize template"""
    import nomenclator.utilities

    if sys.version_info.major < 3:
        expected = expected.replace(r"/", r"\/")
        expected = expected.replace(r"@", r"\@")
        expected = expected.replace(r"C:", r"C\:")

    assert nomenclator.utilities.sanitize_template(template) == expected
