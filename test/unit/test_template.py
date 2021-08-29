# -*- coding: utf-8 -*-

import re
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
