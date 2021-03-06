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


def test_update_comp_scenario1():
    """Return updated context object.

    Incoming context does not have any template configs.

    """
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
        error=None,
        outputs=(
            nomenclator.context.OutputContext(
                name="Write1",
                new_name="Write1",
                blacklisted_names=tuple(),
                path="/path/to/test.dpx",
                old_path="/path/to/test.dpx",
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
                append_passname_to_subfolder=False,
                error=None,
            ),
        )
    )

    _context = nomenclator.context.update(context)

    assert _context.path == ""
    assert _context.version is None
    assert _context.error["message"] == "No template configurations found."
    assert _context.outputs[0].path == ""
    assert _context.outputs[0].destination == ""
    assert _context.outputs[0].destinations == tuple()
    assert _context.outputs[0].error is None


def test_update_comp_scenario2():
    """Return updated context object.

    Incoming context has one template config which requires the "shot"
    token to match the expression "sh\\d+". However, location path has
    a shot folder named "sh004_SPECIAL" which does not match with that
    expression.

    """
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
                append_username_to_name=True,
                outputs=None,
            ),
        ),
        error=None,
        outputs=(
            nomenclator.context.OutputContext(
                name="Write1",
                new_name="Write1",
                blacklisted_names=tuple(),
                path="/path/to/test.dpx",
                old_path="/path/to/test.dpx",
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
                append_passname_to_subfolder=False,
                error=None,
            ),
        )
    )

    _context = nomenclator.context.update(context)

    assert _context.path == ""
    assert _context.version is None
    assert _context.error["message"] == "No matching template configuration found."
    assert _context.outputs[0].path == ""
    assert _context.outputs[0].destination == ""
    assert _context.outputs[0].destinations == tuple()
    assert _context.outputs[0].error is None


def test_update_comp_scenario3():
    """Return updated context object.

    Incoming context has one template config which match with the
    location path. However, this config does not define any output
    template configs.

    """
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
                append_username_to_name=True,
                outputs=tuple(),
            ),
        ),
        error=None,
        outputs=(
            nomenclator.context.OutputContext(
                name="Write1",
                new_name="Write1",
                blacklisted_names=tuple(),
                path="/path/to/test.dpx",
                old_path="/path/to/test.dpx",
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
                append_passname_to_subfolder=False,
                error=None,
            ),
        )
    )

    _context = nomenclator.context.update(context)

    assert _context.path == os.path.join(
        "/path/my_project/ep002/sh004/scripts",
        "my_project_ep002_sh004_v002.nk"
    )
    assert _context.version == 2
    assert _context.error is None
    assert _context.outputs[0].path == ""
    assert _context.outputs[0].destination == ""
    assert _context.outputs[0].destinations == tuple()
    assert _context.outputs[0].error["message"] == "No output template configurations found."


def test_update_comp_scenario4():
    """Return updated context object.

    Incoming context has one template config which match with the
    location path. This config contains an output template config with
    an ID corresponding to the destination required.

    """
    import nomenclator.context
    from nomenclator.config import TemplateConfig, OutputTemplateConfig

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
                append_username_to_name=True,
                outputs=(
                    OutputTemplateConfig(
                        id="comps",
                        pattern_path=r"/path/{project}/{episode:ep\d+}/{shot:sh\d+}/comps",
                        pattern_base=r"{project}_{episode}_{shot}_v{version}",
                        append_username_to_name=False,
                        append_colorspace_to_name=False,
                        append_passname_to_name=False,
                        append_passname_to_subfolder=False,
                    ),
                ),
            ),
        ),
        error=None,
        outputs=(
            nomenclator.context.OutputContext(
                name="Write1",
                new_name="Write1",
                blacklisted_names=tuple(),
                path="/path/to/test.dpx",
                old_path="/path/to/test.dpx",
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
                append_passname_to_subfolder=False,
                error=None,
            ),
        )
    )

    _context = nomenclator.context.update(context)

    assert _context.path == os.path.join(
        "/path/my_project/ep002/sh004/scripts",
        "my_project_ep002_sh004_v002.nk"
    )
    assert _context.version == 2
    assert _context.error is None
    assert _context.outputs[0].path == os.path.join(
        "/path/my_project/ep002/sh004/comps",
        "my_project_ep002_sh004_v002.#.dpx"
    )
    assert _context.outputs[0].destination == "comps"
    assert _context.outputs[0].destinations == ("comps",)
    assert _context.outputs[0].error is None


def test_update_comp_scenario5():
    """Return updated context object.

    Like the scenario 4, incoming context has one template config
    which match with the location path.

    The paths will be generated with the following options:

    * scene: append_username_to_name
    * output append_username_to_name
    * output: append_colorspace_to_name
    * output: append_passname_to_name
    * output: append_passname_to_subfolder

    The output pattern path does not define any subfolders, so the last
    option will be ignored.

    """
    import nomenclator.context
    from nomenclator.config import TemplateConfig, OutputTemplateConfig

    context = nomenclator.context.Context(
        location_path="/path/my_project/ep002/sh004/scripts",
        recent_locations=tuple(),
        path="",
        suffix="nk",
        version=None,
        description="comp",
        descriptions=("comp", "precomp", "roto"),
        append_username_to_name=True,
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
                append_username_to_name=True,
                outputs=(
                    OutputTemplateConfig(
                        id="comps",
                        pattern_path=r"/path/{project}/{episode:ep\d+}/{shot:sh\d+}/comps",
                        pattern_base=r"{project}_{episode}_{shot}_v{version}",
                        append_username_to_name=False,
                        append_colorspace_to_name=False,
                        append_passname_to_name=False,
                        append_passname_to_subfolder=False,
                    ),
                ),
            ),
        ),
        error=None,
        outputs=(
            nomenclator.context.OutputContext(
                name="Write1",
                new_name="Write1",
                blacklisted_names=tuple(),
                path="/path/to/test.dpx",
                old_path="/path/to/test.dpx",
                passname="beauty",
                enabled=True,
                destination="comps",
                destinations=("comps", "precomps", "roto"),
                file_type="dpx",
                file_types=("exr", "dpx", "mov"),
                multi_views=True,
                colorspace="rec709",
                append_username_to_name=True,
                append_colorspace_to_name=True,
                append_passname_to_name=True,
                append_passname_to_subfolder=True,
                error=None,
            ),
        )
    )

    _context = nomenclator.context.update(context)

    assert _context.path == os.path.join(
        "/path/my_project/ep002/sh004/scripts",
        "my_project_ep002_sh004_v002_steve.nk"
    )
    assert _context.version == 2
    assert _context.error is None
    assert _context.outputs[0].path == os.path.join(
        "/path/my_project/ep002/sh004/comps",
        "my_project_ep002_sh004_v002_rec709_steve_beauty_%V.#.dpx"
    )
    assert _context.outputs[0].destination == "comps"
    assert _context.outputs[0].destinations == ("comps",)
    assert _context.outputs[0].error is None


def test_update_comp_scenario6():
    """Return updated context object.

    Like the scenario 5, incoming context has one template config
    which match with the location path. Several options must be
    appended to generated paths.

    This time, the output pattern path define a subfolder.

    """
    import nomenclator.context
    from nomenclator.config import TemplateConfig, OutputTemplateConfig

    context = nomenclator.context.Context(
        location_path="/path/my_project/ep002/sh004/scripts",
        recent_locations=tuple(),
        path="",
        suffix="nk",
        version=None,
        description="comp",
        descriptions=("comp", "precomp", "roto"),
        append_username_to_name=True,
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
                append_username_to_name=True,
                outputs=(
                    OutputTemplateConfig(
                        id="comps",
                        pattern_path=r"/path/{project}/{episode:ep\d+}/{shot:sh\d+}/comps",
                        pattern_base=os.path.join(
                            r"{project}_{episode}",
                            r"{project}_{episode}_{shot}_v{version}"
                        ),
                        append_username_to_name=False,
                        append_colorspace_to_name=False,
                        append_passname_to_name=False,
                        append_passname_to_subfolder=False,
                    ),
                ),
            ),
        ),
        error=None,
        outputs=(
            nomenclator.context.OutputContext(
                name="Write1",
                new_name="Write1",
                blacklisted_names=tuple(),
                path="/path/to/test.dpx",
                old_path="/path/to/test.dpx",
                passname="beauty",
                enabled=True,
                destination="comps",
                destinations=("comps", "precomps", "roto"),
                file_type="dpx",
                file_types=("exr", "dpx", "mov"),
                multi_views=True,
                colorspace="rec709",
                append_username_to_name=True,
                append_colorspace_to_name=True,
                append_passname_to_name=True,
                append_passname_to_subfolder=True,
                error=None,
            ),
        )
    )

    _context = nomenclator.context.update(context)

    assert _context.path == os.path.join(
        "/path/my_project/ep002/sh004/scripts",
        "my_project_ep002_sh004_v002_steve.nk"
    )
    assert _context.version == 2
    assert _context.error is None
    assert _context.outputs[0].path == os.path.join(
        "/path/my_project/ep002/sh004/comps",
        "my_project_ep002_beauty",
        "my_project_ep002_sh004_v002_rec709_steve_beauty_%V.#.dpx"
    )
    assert _context.outputs[0].destination == "comps"
    assert _context.outputs[0].destinations == ("comps",)
    assert _context.outputs[0].error is None


def test_update_comp_scenario7():
    """Return updated context object.

    Same as the scenario 3, but a token value is missing in
    scene pattern base name.

    """
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
                pattern_base=r"{project}_{episode}_{shot}_{foo}_v{version}",
                default_expression=r"[\w_.-]+",
                match_start=True,
                match_end=True,
                append_username_to_name=True,
                outputs=tuple(),
            ),
        ),
        error=None,
        outputs=(
            nomenclator.context.OutputContext(
                name="Write1",
                new_name="Write1",
                blacklisted_names=tuple(),
                path="/path/to/test.dpx",
                old_path="/path/to/test.dpx",
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
                append_passname_to_subfolder=False,
                error=None,
            ),
        )
    )

    _context = nomenclator.context.update(context)

    assert _context.path == ""
    assert _context.version is None
    assert _context.error["message"] == "Template configuration contains an error [Config]"
    assert _context.outputs[0].path == ""
    assert _context.outputs[0].destination == ""
    assert _context.outputs[0].destinations == tuple()
    assert _context.outputs[0].error["message"] == "No output template configurations found."


def test_update_comp_scenario8():
    """Return updated context object.

    Same as the scenario 7, but the missing token value is provided
    via the config

    """
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
        tokens=(("foo", "bar"),),
        username="steve",
        template_configs=(
            TemplateConfig(
                id="Config",
                pattern_path=r"/path/{project}/{episode:ep\d+}/{shot:sh\d+}/scripts",
                pattern_base=r"{project}_{episode}_{shot}_{foo}_v{version}",
                default_expression=r"[\w_.-]+",
                match_start=True,
                match_end=True,
                append_username_to_name=True,
                outputs=tuple(),
            ),
        ),
        error=None,
        outputs=(
            nomenclator.context.OutputContext(
                name="Write1",
                new_name="Write1",
                blacklisted_names=tuple(),
                path="/path/to/test.dpx",
                old_path="/path/to/test.dpx",
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
                append_passname_to_subfolder=False,
                error=None,
            ),
        )
    )

    _context = nomenclator.context.update(context)

    assert _context.path == os.path.join(
        "/path/my_project/ep002/sh004/scripts",
        "my_project_ep002_sh004_bar_v002.nk"
    )
    assert _context.version == 2
    assert _context.error is None
    assert _context.outputs[0].path == ""
    assert _context.outputs[0].destination == ""
    assert _context.outputs[0].destinations == tuple()
    assert _context.outputs[0].error["message"] == "No output template configurations found."


def test_update_comp_scenario9():
    """Return updated context object.

    Same as the scenario 4, but a token value is missing in
    output pattern base name.

    """
    import nomenclator.context
    from nomenclator.config import TemplateConfig, OutputTemplateConfig

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
                append_username_to_name=True,
                outputs=(
                    OutputTemplateConfig(
                        id="comps",
                        pattern_path=r"/path/{project}/{episode:ep\d+}/{shot:sh\d+}/comps",
                        pattern_base=r"{project}_{episode}_{shot}_{foo}_v{version}",
                        append_username_to_name=False,
                        append_colorspace_to_name=False,
                        append_passname_to_name=False,
                        append_passname_to_subfolder=False,
                    ),
                ),
            ),
        ),
        error=None,
        outputs=(
            nomenclator.context.OutputContext(
                name="Write1",
                new_name="Write1",
                blacklisted_names=tuple(),
                path="/path/to/test.dpx",
                old_path="/path/to/test.dpx",
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
                append_passname_to_subfolder=False,
                error=None,
            ),
        )
    )

    _context = nomenclator.context.update(context)

    assert _context.path == os.path.join(
        "/path/my_project/ep002/sh004/scripts",
        "my_project_ep002_sh004_v002.nk"
    )
    assert _context.version == 2
    assert _context.error is None
    assert _context.outputs[0].path == ""
    assert _context.outputs[0].destination == "comps"
    assert _context.outputs[0].destinations == ("comps",)
    assert _context.outputs[0].error["message"] == (
        "Output Template configuration contains an error [comps]"
    )


def test_update_comp_scenario10():
    """Return updated context object.

    Same as the scenario 9, but a token value is missing in
    output pattern base name.

    """
    import nomenclator.context
    from nomenclator.config import TemplateConfig, OutputTemplateConfig

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
        tokens=(("foo", "bar"),),
        username="steve",
        template_configs=(
            TemplateConfig(
                id="Config",
                pattern_path=r"/path/{project}/{episode:ep\d+}/{shot:sh\d+}/scripts",
                pattern_base=r"{project}_{episode}_{shot}_v{version}",
                default_expression=r"[\w_.-]+",
                match_start=True,
                match_end=True,
                append_username_to_name=True,
                outputs=(
                    OutputTemplateConfig(
                        id="comps",
                        pattern_path=r"/path/{project}/{episode:ep\d+}/{shot:sh\d+}/comps",
                        pattern_base=r"{project}_{episode}_{shot}_{foo}_v{version}",
                        append_username_to_name=False,
                        append_colorspace_to_name=False,
                        append_passname_to_name=False,
                        append_passname_to_subfolder=False,
                    ),
                ),
            ),
        ),
        error=None,
        outputs=(
            nomenclator.context.OutputContext(
                name="Write1",
                new_name="Write1",
                blacklisted_names=tuple(),
                path="/path/to/test.dpx",
                old_path="/path/to/test.dpx",
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
                append_passname_to_subfolder=False,
                error=None,
            ),
        )
    )

    _context = nomenclator.context.update(context)

    assert _context.path == os.path.join(
        "/path/my_project/ep002/sh004/scripts",
        "my_project_ep002_sh004_v002.nk"
    )
    assert _context.version == 2
    assert _context.error is None
    assert _context.outputs[0].path == os.path.join(
        "/path/my_project/ep002/sh004/comps",
        "my_project_ep002_sh004_bar_v002.#.dpx"
    )
    assert _context.outputs[0].destination == "comps"
    assert _context.outputs[0].destinations == ("comps",)
    assert _context.outputs[0].error is None
