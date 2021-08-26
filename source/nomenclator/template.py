# -*- coding: utf-8 -*-

import re


def fetch_resolved_tokens(
    path, pattern, default_expression=r"[\w_.-]+",
    match_start=True, match_end=True
):
    """Return resolved tokens from *path* and *pattern* if compatible.

    For instance::

        >>> fetch_resolved_tokens(
        ...     "/path/my_project/ep002/sh003/scripts",
        ...     "/path/{project}/{episode:ep\\d+}/{shot:sh\\d+}/scripts"
        ... )
        {
            "project": "my_project",
            "episode": "ep002",
            "shot": "sh003"
        }

    If the *path* and *pattern* are compatible, but the *pattern* does not
    specify any tokens, an empty mapping will be returned.

        >>> fetch_resolved_tokens(
        ...     "/path/project/scripts",
        ...     "/path/project/scripts"
        ... )
        {}

    If the *path* and *pattern* are not compatible, None is returned.

        >>> fetch_resolved_tokens(
        ...     "/path/my_project/build/character/scripts",
        ...     "/path/{project}/{episode:ep\\d+}/{shot:sh\\d+}/scripts"
        ... )
        None

    :param path: Path to compare template pattern to.

    :param pattern: String representing a template pattern path,
        with or without tokens.

    :param default_expression: Regular expression pattern to use for tokens
        when no expression is specified. Default is ``[\\w_.-]+``.

    :param match_start: Indicate whether the *path* should match against the
        start of the *pattern*. Default is True.

    :param match_end: Indicate whether the *path* should match against the
        end of the *pattern*. Default is True.

    :return: Mapping regrouping resolved token value associated with
        their name, or None if the *path* and *pattern* are not compatible.

    """
    regex = construct_regexp(
        pattern,
        default_expression=default_expression,
        match_start=match_start,
        match_end=match_end
    )

    match = regex.search(path)
    if match:
        return match.groupdict()


def construct_regexp(
    pattern, default_expression=r"[\w_.-]+",
    match_start=True, match_end=True
):
    """Return template pattern converted into a regular expression.

    For instance::

        >>> construct_regexp("/path/{project}/{episode:ep\\d+}")
        re.compile(r"^/path/(?P<project>[\\w_.-]+)/(?P<episode>ep\\d+)$")

    :param pattern: String representing a template pattern path,
        with or without tokens.

    :param default_expression: Regular expression pattern to use for tokens
        when no expression is specified. Default is ``[\\w_.-]+``.

    :param match_start: Indicate whether the regular expression returned
        should match against the start of an input. Default is True.

    :param match_end: Indicate whether the regular expression returned
        should match against the end of an input. Default is True.

    :return: Compiled regular expression.

    """
    pattern = sanitize_pattern(pattern)

    def _convert(match):
        """Return corresponding regular expression."""
        name = match.group("name")
        expression = match.group("expression") or default_expression
        return r"(?P<{0}>{1})".format(name, expression)

    sub_pattern = r"{(?P<name>.+?)(:(?P<expression>.+?))?}"
    pattern = re.sub(sub_pattern, _convert, pattern)

    if match_start:
        pattern = "^" + pattern

    if match_end:
        pattern += "$"

    return re.compile(pattern)


def sanitize_pattern(pattern):
    """Return template pattern with all special characters escaped.

    Tokens name and expressions are returned unchanged.

    For instance::

        >>> sanitize_pattern("/path*/{job:J_.*}")
        "/path\\*/{job:J_.*}"

    :param pattern: String representing a template pattern path,
        with or without tokens.

    :return: Sanitized string template pattern.

    """

    def _escape(match):
        """Escape 'other' group value if required."""
        groups = match.groupdict()
        if groups["other"] is not None:
            return re.escape(groups["other"])

        return groups["token"]

    sub_pattern = r"(?P<token>{(.+?)(:.+?)?})|(?P<other>.+?)"
    return re.sub(sub_pattern, _escape, pattern)
