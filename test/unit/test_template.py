# -*- coding: utf-8 -*-

import re
import os
import sys

import pytest


@pytest.fixture()
def mocked_construct_regexp(mocker):
    """Return mocked 'nomenclator.template.construct_regexp' function."""
    import nomenclator.template
    return mocker.patch.object(nomenclator.template, "construct_regexp")


@pytest.fixture()
def mocked_sanitize_pattern(mocker):
    """Return mocked 'nomenclator.template.sanitize_pattern' function."""
    import nomenclator.template
    return mocker.patch.object(nomenclator.template, "sanitize_pattern")


@pytest.fixture()
def mocked_resolve(mocker):
    """Return mocked 'nomenclator.utilities.resolve' function."""
    import nomenclator.template
    return mocker.patch.object(nomenclator.template, "resolve")


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


@pytest.mark.parametrize("options, token_mapping", [
    ({}, {}),
    ({"token_mapping": {"key": "value"}}, {"key": "value"}),
], ids=[
    "simple",
    "with-tokens",
])
def test_generate_scene_name(mocked_resolve, options, token_mapping):
    """Generate scene name from pattern."""
    import nomenclator.template

    result = nomenclator.template.generate_scene_name("BASE_NAME", "nk", **options)
    assert result == mocked_resolve.return_value

    mocked_resolve.assert_called_once_with("BASE_NAME.nk", token_mapping)


def test_generate_scene_name_with_username(mocked_resolve):
    """Generate scene name from pattern with username appended to base."""
    import nomenclator.template

    result = nomenclator.template.generate_scene_name(
        "BASE_NAME", "nk",
        append_username=True,
        token_mapping="__TOKEN_MAPPING__"
    )
    assert result == mocked_resolve.return_value

    mocked_resolve.assert_called_once_with(
        "BASE_NAME_{username}.nk", "__TOKEN_MAPPING__"
    )


@pytest.mark.parametrize("options, token_mapping", [
    ({}, {}),
    ({"token_mapping": {"key": "value"}}, {"key": "value"}),
], ids=[
    "simple",
    "with-tokens",
])
def test_generate_output_name(mocked_resolve, options, token_mapping):
    """Generate output name from pattern."""
    import nomenclator.template

    result = nomenclator.template.generate_output_name("BASE_NAME", "mp4", **options)
    assert result == mocked_resolve.return_value

    mocked_resolve.assert_called_once_with("BASE_NAME.mp4", token_mapping)


def test_generate_output_name_with_subfolder(mocked_resolve):
    """Generate scene name from pattern with subfolder."""
    import nomenclator.template

    pattern = os.path.join("folder", "BASE_NAME")

    result = nomenclator.template.generate_output_name(
        pattern, "mp4", token_mapping="__TOKEN_MAPPING__"
    )
    assert result == mocked_resolve.return_value

    mocked_resolve.assert_called_once_with(
        os.path.join("folder", "BASE_NAME.mp4"), "__TOKEN_MAPPING__"
    )


def test_generate_output_name_with_padding(mocked_resolve):
    """Generate scene name from pattern with padding appended to base."""
    import nomenclator.template

    result = nomenclator.template.generate_output_name(
        "BASE_NAME", "exr",
        token_mapping="__TOKEN_MAPPING__"
    )
    assert result == mocked_resolve.return_value

    mocked_resolve.assert_called_once_with(
        "BASE_NAME.{padding}.exr", "__TOKEN_MAPPING__"
    )


def test_generate_output_name_with_passname_in_subfolder(mocked_resolve):
    """Generate scene name from pattern with passname appended to subfolder."""
    import nomenclator.template

    pattern = os.path.join("folder", "BASE_NAME")

    result = nomenclator.template.generate_output_name(
        pattern, "mp4",
        append_passname_to_subfolder=True,
        token_mapping="__TOKEN_MAPPING__"
    )
    assert result == mocked_resolve.return_value

    mocked_resolve.assert_called_once_with(
        os.path.join("folder_{passname}", "BASE_NAME.mp4"), "__TOKEN_MAPPING__"
    )


def test_generate_output_name_with_passname_in_subfolder_error(mocked_resolve):
    """Fail to generate scene name from pattern with passname appended to subfolder."""
    import nomenclator.template

    result = nomenclator.template.generate_output_name(
        "BASE_NAME", "mp4",
        append_passname_to_subfolder=True,
        token_mapping="__TOKEN_MAPPING__"
    )
    assert result == mocked_resolve.return_value

    mocked_resolve.assert_called_once_with(
        "BASE_NAME.mp4", "__TOKEN_MAPPING__"
    )


def test_generate_output_name_with_passname(mocked_resolve):
    """Generate scene name from pattern with passname appended to base."""
    import nomenclator.template

    pattern = os.path.join("folder", "BASE_NAME")

    result = nomenclator.template.generate_output_name(
        pattern, "mp4",
        append_passname=True,
        token_mapping="__TOKEN_MAPPING__"
    )
    assert result == mocked_resolve.return_value

    mocked_resolve.assert_called_once_with(
        os.path.join("folder", "BASE_NAME_{passname}.mp4"),
        "__TOKEN_MAPPING__"
    )


def test_generate_output_name_with_colorspace(mocked_resolve):
    """Generate scene name from pattern with colorspace appended to base."""
    import nomenclator.template

    pattern = os.path.join("folder", "BASE_NAME")

    result = nomenclator.template.generate_output_name(
        pattern, "mp4",
        append_colorspace=True,
        token_mapping="__TOKEN_MAPPING__"
    )
    assert result == mocked_resolve.return_value

    mocked_resolve.assert_called_once_with(
        os.path.join("folder", "BASE_NAME_{colorspace}.mp4"),
        "__TOKEN_MAPPING__"
    )


def test_generate_output_name_with_username(mocked_resolve):
    """Generate scene name from pattern with username appended to base."""
    import nomenclator.template

    pattern = os.path.join("folder", "BASE_NAME")

    result = nomenclator.template.generate_output_name(
        pattern, "mp4",
        append_username=True,
        token_mapping="__TOKEN_MAPPING__"
    )
    assert result == mocked_resolve.return_value

    mocked_resolve.assert_called_once_with(
        os.path.join("folder", "BASE_NAME_{username}.mp4"),
        "__TOKEN_MAPPING__"
    )


def test_generate_output_name_with_multi_views(mocked_resolve):
    """Generate scene name from pattern with multi views appended to base."""
    import nomenclator.template

    pattern = os.path.join("folder", "BASE_NAME")

    result = nomenclator.template.generate_output_name(
        pattern, "mp4",
        multi_views=True,
        token_mapping="__TOKEN_MAPPING__"
    )
    assert result == mocked_resolve.return_value

    mocked_resolve.assert_called_once_with(
        os.path.join("folder", "BASE_NAME_%V.mp4"),
        "__TOKEN_MAPPING__"
    )


def test_generate_output_name_with_several_options(mocked_resolve):
    """Generate scene name from pattern with several options."""
    import nomenclator.template

    pattern = os.path.join("folder", "BASE_NAME")

    result = nomenclator.template.generate_output_name(
        pattern, "exr",
        append_passname_to_subfolder=True,
        append_passname=True,
        append_colorspace=True,
        append_username=True,
        multi_views=True,
        token_mapping="__TOKEN_MAPPING__"
    )
    assert result == mocked_resolve.return_value

    mocked_resolve.assert_called_once_with(
        os.path.join(
            "folder_{passname}",
            "BASE_NAME_{colorspace}_{username}_{passname}_%V.{padding}.exr"
        ),
        "__TOKEN_MAPPING__"
    )


def test_resolve():
    """Resolve name."""
    import nomenclator.template

    pattern = os.path.join(
        "folder_{passname}",
        "{project}_{shot}_{description}_v{version}"
        "_{colorspace}_{username}_{passname}_%V.%01d.exr"
    )

    token_mapping = {
        "project": "test",
        "shot": "sh003",
        "description": "comp",
        "version": "002",
        "username": "steve",
        "colorspace": "rec709",
        "passname": "beauty",
    }

    name = nomenclator.template.resolve(pattern, token_mapping)
    assert name == os.path.join(
        "folder_beauty", "test_sh003_comp_v002_rec709_steve_beauty_%V.%01d.exr"
    )


def test_resolve_with_discarded_expression():
    """Resolve name with discarded expression."""
    import nomenclator.template

    pattern = os.path.join(
        r"folder_{passname:\w+}",
        r"{project}_{shot:sh\d+}_{description}_v{version:\d+}"
        r"_{colorspace}_{username}_{passname:.*?}_%V.%01d.exr"
    )

    token_mapping = {
        "project": "test",
        "shot": "sh003",
        "description": "comp",
        "version": "002",
        "username": "steve",
        "colorspace": "rec709",
        "passname": "beauty",
    }

    name = nomenclator.template.resolve(pattern, token_mapping)
    assert name == os.path.join(
        "folder_beauty",
        "test_sh003_comp_v002_rec709_steve_beauty_%V.%01d.exr"
    )


def test_resolve_without_tokens():
    """Resolve name without tokens."""
    import nomenclator.template
    assert nomenclator.template.resolve("BASE_NAME", {}) == "BASE_NAME"


def test_resolve_with_missing_token():
    """Resolve name without tokens."""
    import nomenclator.template

    with pytest.raises(ValueError) as error:
        nomenclator.template.resolve("{foo}", {})

    assert str(error.value) == "Missing token value: 'foo'"
