# -*- coding: utf-8 -*-

import pytest


@pytest.fixture()
def mocked_fetch_nodes(mocker):
    """Return mocked 'nomenclator.utilities.fetch_nodes' function."""
    import nomenclator.utilities
    return mocker.patch.object(nomenclator.utilities, "fetch_nodes", )


@pytest.fixture()
def mocked_fetch_outputs(mocker):
    """Return mocked 'nomenclator.context.fetch_outputs' function."""
    import nomenclator.context
    return mocker.patch.object(nomenclator.context, "fetch_outputs")


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


def test_fetch(
    mocker, mocked_fetch_outputs, mocked_fetch_paddings,
    mocked_fetch_recent_comp_paths
):
    """Return context object."""
    import nomenclator.context

    config = mocker.Mock(max_padding=10, max_locations=15)
    context = nomenclator.context.fetch(config)

    assert context == nomenclator.context.Context(
        location_path=None,
        recent_locations=mocked_fetch_recent_comp_paths.return_value,
        path=None,
        description=None,
        descriptions=config.descriptions,
        append_username_to_name=False,
        padding=None,
        paddings=mocked_fetch_paddings.return_value,
        create_subfolders=config.create_subfolders,
        outputs=tuple()
    )

    mocked_fetch_outputs.assert_not_called()
    mocked_fetch_paddings.assert_called_once_with(max_value=10)
    mocked_fetch_recent_comp_paths.assert_called_once_with(max_values=15)


def test_fetch_with_outputs(
    mocker, mocked_fetch_outputs, mocked_fetch_paddings,
    mocked_fetch_recent_comp_paths
):
    """Return context object with output contexts."""
    import nomenclator.context

    config = mocker.Mock(max_padding=10, max_locations=15)
    context = nomenclator.context.fetch(config, with_outputs=True)

    assert context == nomenclator.context.Context(
        location_path=None,
        recent_locations=mocked_fetch_recent_comp_paths.return_value,
        path=None,
        description=None,
        descriptions=config.descriptions,
        append_username_to_name=False,
        padding=None,
        paddings=mocked_fetch_paddings.return_value,
        create_subfolders=config.create_subfolders,
        outputs=mocked_fetch_outputs.return_value
    )

    mocked_fetch_outputs.assert_called_once()
    mocked_fetch_paddings.assert_called_once_with(max_value=10)
    mocked_fetch_recent_comp_paths.assert_called_once_with(max_values=15)


def test_fetch_outputs(mocker, mocked_fetch_nodes):
    """Return output context objects."""
    import nomenclator.context

    knob_mappings = [
        {
            "file": mocker.Mock(**{"value.return_value": ""}),
            "disable": mocker.Mock(**{"value.return_value": False}),
            "file_type": mocker.Mock(**{
                "value.return_value": "",
                "values.return_value": ["exr", "dpx", "tiff", "mov\t\t\tffmpeg"]
            }),
        },
        {
            "file": mocker.Mock(**{"value.return_value": "/path/to/file.dpx"}),
            "disable": mocker.Mock(**{"value.return_value": False}),
            "file_type": mocker.Mock(**{
                "value.return_value": "dpx",
                "values.return_value": ["exr", "dpx", "tiff", "mov\t\t\tffmpeg"],

            }),
        },
        {
            "file": mocker.Mock(**{"value.return_value": ""}),
            "disable": mocker.Mock(**{"value.return_value": True}),
            "file_type": mocker.Mock(**{
                "value.return_value": "",
                "values.return_value": ["exr", "abc"]
            }),
        }
    ]

    nodes = [
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

    mocked_fetch_nodes.return_value = (
        nodes, ["node1", "node2", "node3", "node4", "node5"]
    )

    contexts = nomenclator.context.fetch_outputs()

    assert contexts == (
        nomenclator.context.OutputContext(
            name="node1",
            blacklisted_names=("node2", "node3", "node4", "node5"),
            path="",
            passname="node1",
            enabled=True,
            destination=None,
            destinations=tuple(),
            file_type="exr",
            file_types=("exr", "dpx", "tiff", "mov"),
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
            destination=None,
            destinations=tuple(),
            file_type="dpx",
            file_types=("exr", "dpx", "tiff", "mov"),
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
            destination=None,
            destinations=tuple(),
            file_type="exr",
            file_types=("exr", "abc"),
            append_username_to_name=False,
            append_colorspace_to_name=False,
            append_passname_to_name=False,
            append_passname_to_subfolder=False
        ),
    )
