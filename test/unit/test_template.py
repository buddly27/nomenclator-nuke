# -*- coding: utf-8 -*-

import re
import os
import sys

import pytest


@pytest.fixture()
def mocked_construct_regexp(mocker):
    """Return mocked 'nomenclator.utilities.construct_regexp' function."""
    import nomenclator.template
    return mocker.patch.object(nomenclator.template, "construct_regexp")


@pytest.fixture()
def mocked_sanitize_pattern(mocker):
    """Return mocked 'nomenclator.utilities.sanitize_pattern' function."""
    import nomenclator.template
    return mocker.patch.object(nomenclator.template, "sanitize_pattern")


@pytest.mark.parametrize(
    "options, default_expression, match_start, match_end", [
        ({}, r"[\w_.-]+", True, True),
        ({"default_expression": r"\w+"}, r"\w+", True, True),
        ({"match_start": False}, r"[\w_.-]+", False, True),
        ({"match_end": False}, r"[\w_.-]+", True, False),
    ],
    ids=[
        "simple",
        "with-default-expression",
        "without-match-start",
        "without-match-end",
    ]
)
def test_fetch_resolved_tokens(
    mocked_construct_regexp, options, default_expression,
    match_start, match_end
):
    """Return resolved token mapping."""
    import nomenclator.template

    path = "/path/my_project/ep002/sh003/scripts"
    regexp = re.compile(
        r"^/path/(?P<project>[\w_.\-]+)/(?P<episode>ep\d+)/"
        r"(?P<shot>sh\d+)/scripts$"
    )

    mocked_construct_regexp.return_value = regexp

    data = nomenclator.template.fetch_resolved_tokens(
        path, "__PATTERN__", **options
    )

    assert data == {
        "project": "my_project",
        "episode": "ep002",
        "shot": "sh003",
    }

    mocked_construct_regexp.assert_called_once_with(
        "__PATTERN__",
        default_expression=default_expression,
        match_start=match_start,
        match_end=match_end
    )


@pytest.mark.parametrize(
    "options, default_expression, match_start, match_end", [
        ({}, r"[\w_.-]+", True, True),
        ({"default_expression": r"\w+"}, r"\w+", True, True),
        ({"match_start": False}, r"[\w_.-]+", False, True),
        ({"match_end": False}, r"[\w_.-]+", True, False),
    ],
    ids=[
        "simple",
        "with-default-expression",
        "without-match-start",
        "without-match-end",
    ]
)
def test_fetch_resolved_tokens_incompatible(
    mocked_construct_regexp, options, default_expression,
    match_start, match_end
):
    """Fail to return resolved token mapping."""
    import nomenclator.template

    path = "/path/my_project/build/character/scripts"
    regexp = re.compile(
        r"^/path/(?P<project>[\w_.\-]+)/(?P<episode>ep\d+)/"
        r"(?P<shot>sh\d+)/scripts$"
    )

    mocked_construct_regexp.return_value = regexp

    data = nomenclator.template.fetch_resolved_tokens(
        path, "__PATTERN__", **options
    )

    assert data is None

    mocked_construct_regexp.assert_called_once_with(
        "__PATTERN__",
        default_expression=default_expression,
        match_start=match_start,
        match_end=match_end
    )


def test_construct_regexp_without_tokens(mocked_sanitize_pattern):
    """Create regular expression without tokens."""
    template = r"/path/project/episode"
    mocked_sanitize_pattern.return_value = template

    import nomenclator.template
    regexp = nomenclator.template.construct_regexp(template)
    assert regexp == re.compile(r"^/path/project/episode$")

    mocked_sanitize_pattern.assert_called_once_with(template)


def test_construct_regexp_with_tokens(mocked_sanitize_pattern):
    """Create regular expression with tokens."""
    template = r"/path/{project}/{episode}"
    mocked_sanitize_pattern.return_value = template

    import nomenclator.template
    regexp = nomenclator.template.construct_regexp(template)
    assert regexp == re.compile(
        r"^/path/(?P<project>[\w_.-]+)/(?P<episode>[\w_.-]+)$"
    )

    mocked_sanitize_pattern.assert_called_once_with(template)


def test_construct_regexp_with_token_expressions(mocked_sanitize_pattern):
    """Create regular expression with tokens containing expressions."""
    template = r"/path/{project}/{episode:ep\d+}"
    mocked_sanitize_pattern.return_value = template

    import nomenclator.template
    regexp = nomenclator.template.construct_regexp(template)
    assert regexp == re.compile(
        r"^/path/(?P<project>[\w_.-]+)/(?P<episode>ep\d+)$"
    )

    mocked_sanitize_pattern.assert_called_once_with(template)


def test_construct_regexp_with_default_expression(mocked_sanitize_pattern):
    """Create regular expression with default expression."""
    template = r"/path/{project}/{episode:ep\d+}"
    mocked_sanitize_pattern.return_value = template

    import nomenclator.template
    regexp = nomenclator.template.construct_regexp(
        template, default_expression=r"\w+"
    )
    assert regexp == re.compile(
        r"^/path/(?P<project>\w+)/(?P<episode>ep\d+)$"
    )

    mocked_sanitize_pattern.assert_called_once_with(template)


def test_construct_regexp_without_start_anchor(mocked_sanitize_pattern):
    """Create regular expression without start anchor."""
    template = r"/path/{project}/{episode:ep\d+}"
    mocked_sanitize_pattern.return_value = template

    import nomenclator.template
    regexp = nomenclator.template.construct_regexp(
        template, match_start=False
    )
    assert regexp == re.compile(
        r"/path/(?P<project>[\w_.-]+)/(?P<episode>ep\d+)$"
    )

    mocked_sanitize_pattern.assert_called_once_with(template)


def test_construct_regexp_without_end_anchor(mocked_sanitize_pattern):
    """Create regular expression without end anchor."""
    template = r"/path/{project}/{episode:ep\d+}"
    mocked_sanitize_pattern.return_value = template

    import nomenclator.template
    regexp = nomenclator.template.construct_regexp(
        template, match_end=False
    )
    assert regexp == re.compile(
        r"^/path/(?P<project>[\w_.-]+)/(?P<episode>ep\d+)"
    )

    mocked_sanitize_pattern.assert_called_once_with(template)


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
        r"/^p@th./{project:J_.*}/{episode:ep\d+}",
        r"/\^p@th\./{project:J_.*}/{episode:ep\d+}",
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
        r"C:\\^p@th.\{project:J_.*}\{episode:ep\d+}",
        r"C:\\\\\^p@th\.\\{project:J_.*}\\{episode:ep\d+}",
    ),
], ids=[
    "unix-path-without-tokens",
    "unix-path-with-tokens",
    "unix-path-with-tokens-and-patterns",
    "windows-path-without-tokens",
    "windows-path-with-tokens",
    "windows-path-with-tokens-and-patterns",
])
def test_sanitize_pattern(template, expected):
    """Sanitize pattern"""
    import nomenclator.template

    if sys.version_info.major < 3:
        expected = expected.replace(r"/", r"\/")
        expected = expected.replace(r"@", r"\@")
        expected = expected.replace(r"C:", r"C\:")

    assert nomenclator.template.sanitize_pattern(template) == expected


def test_generate_scene_name_without_tokens():
    """Generate scene name from pattern without any tokens."""
    import nomenclator.template

    pattern = "base_name"

    result = nomenclator.template.generate_scene_name(pattern, "nk")
    assert result == "base_name.nk"

    result = nomenclator.template.generate_scene_name(
        pattern, "nk", token_mapping={"key": "value"}
    )
    assert result == "base_name.nk"


def test_generate_scene_name_with_tokens():
    """Generate scene name from pattern with tokens."""
    import nomenclator.template

    pattern = "{project}_{shot}_{description}_v{version}"

    result = nomenclator.template.generate_scene_name(
        pattern, "nk", token_mapping={
            "project": "test",
            "shot": "sh003",
            "description": "comp",
            "version": "002",
        }
    )
    assert result == "test_sh003_comp_v002.nk"


def test_generate_scene_name_with_tokens_error():
    """Fail to generate scene name from pattern when value is missing from token."""
    import nomenclator.template

    pattern = "{project}_{shot}_{description}_v{version}"

    with pytest.raises(KeyError) as error:
        nomenclator.template.generate_scene_name(
            pattern, "nk", token_mapping={
                "shot": "sh003",
                "description": "comp",
                "version": "002",
            }
        )

    assert str(error.value) == "'project'"


def test_generate_scene_name_with_username():
    """Generate scene name from pattern with username appended to base."""
    import nomenclator.template

    pattern = "base_name"
    result = nomenclator.template.generate_scene_name(
        pattern, "nk",
        append_username=True,
        token_mapping={
            "username": "steve",
        }
    )
    assert result == "base_name_steve.nk"

    pattern = "{project}_{shot}_{description}_v{version}"
    result = nomenclator.template.generate_scene_name(
        pattern, "nk",
        append_username=True,
        token_mapping={
            "project": "test",
            "shot": "sh003",
            "description": "comp",
            "version": "002",
            "username": "steve",
        }
    )
    assert result == "test_sh003_comp_v002_steve.nk"


def test_generate_output_name_without_tokens():
    """Generate output name from pattern without any tokens."""
    import nomenclator.template

    pattern = "base_name"

    result = nomenclator.template.generate_output_name(pattern, "exr")
    assert result == "base_name.exr"

    result = nomenclator.template.generate_output_name(
        pattern, "exr", token_mapping={"key": "value"}
    )
    assert result == "base_name.exr"


def test_generate_output_name_with_tokens():
    """Generate output name from pattern with tokens."""
    import nomenclator.template

    pattern = "{project}_{shot}_{description}_v{version}"

    result = nomenclator.template.generate_output_name(
        pattern, "exr", token_mapping={
            "project": "test",
            "shot": "sh003",
            "description": "comp",
            "version": "002",
        }
    )
    assert result == "test_sh003_comp_v002.exr"


def test_generate_output_name_with_tokens_error():
    """Fail to generate output name from pattern when value is missing from token."""
    import nomenclator.template

    pattern = "{project}_{shot}_{description}_v{version}"

    with pytest.raises(KeyError) as error:
        nomenclator.template.generate_output_name(
            pattern, "exr", token_mapping={
                "shot": "sh003",
                "description": "comp",
                "version": "002",
            }
        )

    assert str(error.value) == "'project'"


def test_generate_output_name_with_padding():
    """Generate output name from pattern with padding."""
    import nomenclator.template

    pattern = "base_name"
    result = nomenclator.template.generate_output_name(
        pattern, "exr",
        padding="%01d"
    )
    assert result == "base_name.%01d.exr"

    pattern = "{project}_{shot}_{description}_v{version}"
    result = nomenclator.template.generate_output_name(
        pattern, "exr",
        padding="%01d",
        token_mapping={
            "project": "test",
            "shot": "sh003",
            "description": "comp",
            "version": "002",
        }
    )
    assert result == "test_sh003_comp_v002.%01d.exr"


def test_generate_output_name_with_multi_views():
    """Generate output name from pattern with multi views appended to base."""
    import nomenclator.template

    pattern = "base_name"
    result = nomenclator.template.generate_output_name(
        pattern, "exr",
        multi_views=True
    )
    assert result == "base_name_%V.exr"

    pattern = "{project}_{shot}_{description}_v{version}"
    result = nomenclator.template.generate_output_name(
        pattern, "exr",
        multi_views=True,
        token_mapping={
            "project": "test",
            "shot": "sh003",
            "description": "comp",
            "version": "002",
        }
    )
    assert result == "test_sh003_comp_v002_%V.exr"


def test_generate_output_name_with_colorspace():
    """Generate output name from pattern with colorspace appended to base."""
    import nomenclator.template

    pattern = "base_name"
    result = nomenclator.template.generate_output_name(
        pattern, "exr",
        append_colorspace=True,
        token_mapping={
            "colorspace": "r709"
        }
    )
    assert result == "base_name_r709.exr"

    pattern = "{project}_{shot}_{description}_v{version}"
    result = nomenclator.template.generate_output_name(
        pattern, "exr",
        append_colorspace=True,
        token_mapping={
            "project": "test",
            "shot": "sh003",
            "description": "comp",
            "version": "002",
            "colorspace": "r709"
        }
    )
    assert result == "test_sh003_comp_v002_r709.exr"


def test_generate_output_name_with_username():
    """Generate output name from pattern with username appended to base."""
    import nomenclator.template

    pattern = "base_name"
    result = nomenclator.template.generate_output_name(
        pattern, "exr",
        append_username=True,
        token_mapping={
            "username": "steve"
        }
    )
    assert result == "base_name_steve.exr"

    pattern = "{project}_{shot}_{description}_v{version}"
    result = nomenclator.template.generate_output_name(
        pattern, "exr",
        append_username=True,
        token_mapping={
            "project": "test",
            "shot": "sh003",
            "description": "comp",
            "version": "002",
            "username": "steve"
        }
    )
    assert result == "test_sh003_comp_v002_steve.exr"


def test_generate_output_name_with_passname():
    """Generate output name from pattern with passname appended to base."""
    import nomenclator.template

    pattern = "base_name"
    result = nomenclator.template.generate_output_name(
        pattern, "exr",
        append_passname=True,
        token_mapping={
            "passname": "beauty"
        }
    )
    assert result == "base_name_beauty.exr"

    pattern = "{project}_{shot}_{description}_v{version}"
    result = nomenclator.template.generate_output_name(
        pattern, "exr",
        append_passname=True,
        token_mapping={
            "project": "test",
            "shot": "sh003",
            "description": "comp",
            "version": "002",
            "passname": "beauty"
        }
    )
    assert result == "test_sh003_comp_v002_beauty.exr"


def test_generate_output_name_with_subfolder():
    """Generate output name from pattern with subfolder."""
    import nomenclator.template

    pattern = "path/to/folder/base_name"
    result = nomenclator.template.generate_output_name(
        pattern, "exr",
    )
    assert result == "path/to/folder/base_name.exr"

    pattern = "path/to/folder/{project}_{shot}_{description}_v{version}"
    result = nomenclator.template.generate_output_name(
        pattern, "exr",
        token_mapping={
            "project": "test",
            "shot": "sh003",
            "description": "comp",
            "version": "002",
        }
    )
    assert result == "path/to/folder/test_sh003_comp_v002.exr"


def test_generate_output_name_with_subfolder_username():
    """Generate output name from pattern with username appended to subfolder."""
    import nomenclator.template

    pattern = os.path.join("folder", "base_name")
    result = nomenclator.template.generate_output_name(
        pattern, "exr",
        append_passname_to_subfolder=True,
        token_mapping={
            "passname": "beauty",
        }
    )
    assert result == os.path.join("folder_beauty", "base_name.exr")

    pattern = os.path.join("folder", "{project}_{shot}_{description}_v{version}")
    result = nomenclator.template.generate_output_name(
        pattern, "exr",
        append_passname_to_subfolder=True,
        token_mapping={
            "project": "test",
            "shot": "sh003",
            "description": "comp",
            "version": "002",
            "passname": "beauty",
        }
    )
    assert result == os.path.join("folder_beauty", "test_sh003_comp_v002.exr")


def test_generate_output_name_with_subfolder_username_error():
    """Fail to Generate output name from pattern with username appended to subfolder."""
    import nomenclator.template

    pattern = "base_name"
    result = nomenclator.template.generate_output_name(
        pattern, "exr",
        append_passname_to_subfolder=True
    )
    assert result == "base_name.exr"

    pattern = "{project}_{shot}_{description}_v{version}"
    result = nomenclator.template.generate_output_name(
        pattern, "exr",
        append_passname_to_subfolder=True,
        token_mapping={
            "project": "test",
            "shot": "sh003",
            "description": "comp",
            "version": "002",
        }
    )
    assert result == "test_sh003_comp_v002.exr"


def test_generate_output_name_complex():
    """Fail to Generate output name from pattern with many tokens."""
    import nomenclator.template

    pattern = os.path.join("folder", "{project}_{shot}_{description}_v{version}")
    result = nomenclator.template.generate_output_name(
        pattern, "exr",
        append_passname=True,
        append_username=True,
        append_colorspace=True,
        append_passname_to_subfolder=True,
        multi_views=True,
        padding="%02d",
        token_mapping={
            "project": "test",
            "shot": "sh003",
            "description": "comp",
            "version": "002",
            "username": "steve",
            "colorspace": "r709",
            "passname": "beauty",
        }
    )
    assert result == os.path.join(
        "folder_beauty", "test_sh003_comp_v002_r709_steve_beauty_%V.%02d.exr"
    )
