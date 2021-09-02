# -*- coding: utf-8 -*-

import os

import pytest


@pytest.fixture(autouse=True)
def mock_fetch_next_version(mocker):
    """Mock 'nomenclator.utilities.fetch_next_version' function."""
    import nomenclator.utilities
    return mocker.patch.object(
        nomenclator.utilities, "fetch_next_version", return_value=2
    )


def test_update_comp_without_config():
    """Update context with no template configs."""
    import nomenclator.context

    context = nomenclator.context.Context(
        location_path="/path/my_project/ep002/sh004/scripts",
        recent_locations=tuple(),
        path="",
        suffix="nk",
        version=None,
        description="comp",
        descriptions=("comp", "precomp", "roto"),
        append_username_to_name=False,
        padding="#",
        paddings=("#", "##", "###"),
        create_subfolders=False,
        tokens=tuple(),
        username="steve",
        template_configs=tuple(),
        outputs=(
            nomenclator.context.OutputContext(
                name="Write1",
                blacklisted_names=tuple(),
                path="/path/to/test.dpx",
                passname="beauty",
                enabled=True,
                destination="comps",
                destinations=("comps", "precomps", "roto"),
                file_type="dpx",
                file_types=("exr", "dpx", "mov"),
                multi_views=False,
                colorspace="rec709",
                append_username_to_name=False,
                append_colorspace_to_name=False,
                append_passname_to_name=False,
                append_passname_to_subfolder=False
            ),
        )
    )

    _context = nomenclator.context.update(context)

    assert _context.path == ""
    assert _context.version is None
    assert _context.outputs[0].path == ""


def test_update_comp_no_matching():
    """Update context with no template config matching."""
    import nomenclator.context
    from nomenclator.config import TemplateConfig

    context = nomenclator.context.Context(
        location_path="/path/my_project/ep002/sh004_SPECIAL/scripts",
        recent_locations=tuple(),
        path="",
        suffix="nk",
        version=None,
        description="comp",
        descriptions=("comp", "precomp", "roto"),
        append_username_to_name=False,
        padding="#",
        paddings=("#", "##", "###"),
        create_subfolders=False,
        tokens=tuple(),
        username="steve",
        template_configs=(
            TemplateConfig(
                id="Config",
                pattern_path=r"/path/{project}/{episode:ep\d+}/{shot:sh\d+}/scripts",
                pattern_base=r"{project}_{episode}_{shot}_v{version}",
                default_expression=r"[\w_.-]+",
                match_start=True,
                match_end=True,
                outputs=None,
            ),
        ),
        outputs=(
            nomenclator.context.OutputContext(
                name="Write1",
                blacklisted_names=tuple(),
                path="/path/to/test.dpx",
                passname="beauty",
                enabled=True,
                destination="comps",
                destinations=("comps", "precomps", "roto"),
                file_type="dpx",
                file_types=("exr", "dpx", "mov"),
                multi_views=False,
                colorspace="rec709",
                append_username_to_name=False,
                append_colorspace_to_name=False,
                append_passname_to_name=False,
                append_passname_to_subfolder=False
            ),
        )
    )

    _context = nomenclator.context.update(context)

    assert _context.path == ""
    assert _context.version is None
    assert _context.outputs[0].path == ""


def test_update_comp_matching():
    """Update context with no template config matching."""
    import nomenclator.context
    from nomenclator.config import TemplateConfig

    context = nomenclator.context.Context(
        location_path="/path/my_project/ep002/sh004/scripts",
        recent_locations=tuple(),
        path="",
        suffix="nk",
        version=None,
        description="comp",
        descriptions=("comp", "precomp", "roto"),
        append_username_to_name=False,
        padding="#",
        paddings=("#", "##", "###"),
        create_subfolders=False,
        tokens=tuple(),
        username="steve",
        template_configs=(
            TemplateConfig(
                id="Config",
                pattern_path=r"/path/{project}/{episode:ep\d+}/{shot:sh\d+}/scripts",
                pattern_base=r"{project}_{episode}_{shot}_v{version}",
                default_expression=r"[\w_.-]+",
                match_start=True,
                match_end=True,
                outputs=(
                    TemplateConfig(
                        id="comps",
                        pattern_path=r"/path/{project}/{episode:ep\d+}/{shot:sh\d+}/comps",
                        pattern_base=r"{project}_{episode}_{shot}_v{version}",
                        default_expression=r"[\w_.-]+",
                        match_start=True,
                        match_end=True,
                        outputs=None
                    ),
                ),
            ),
        ),
        outputs=(
            nomenclator.context.OutputContext(
                name="Write1",
                blacklisted_names=tuple(),
                path="/path/to/test.dpx",
                passname="beauty",
                enabled=True,
                destination="comps",
                destinations=("comps", "precomps", "roto"),
                file_type="dpx",
                file_types=("exr", "dpx", "mov"),
                multi_views=False,
                colorspace="rec709",
                append_username_to_name=False,
                append_colorspace_to_name=False,
                append_passname_to_name=False,
                append_passname_to_subfolder=False
            ),
        )
    )

    _context = nomenclator.context.update(context)

    assert _context.path == os.path.join(
        "/path/my_project/ep002/sh004/scripts",
        "my_project_ep002_sh004_v002.nk"
    )
    assert _context.version == 2
    assert _context.outputs[0].path == os.path.join(
        "/path/my_project/ep002/sh004/comps",
        "my_project_ep002_sh004_v002.#.dpx"
    )
