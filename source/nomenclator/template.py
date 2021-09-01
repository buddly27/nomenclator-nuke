# -*- coding: utf-8 -*-

import re
import os

from nomenclator.symbol import DEFAULT_EXPRESSION, VIDEO_TYPES


def fetch_resolved_tokens(
    path, pattern, default_expression=DEFAULT_EXPRESSION,
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
        when no expression is specified. Default is
        :data:`nomanclator.symbol.DEFAULT_EXPRESSION`.

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
    pattern, default_expression=DEFAULT_EXPRESSION,
    match_start=True, match_end=True
):
    """Return template pattern converted into a regular expression.

    For instance::

        >>> construct_regexp("/path/{project}/{episode:ep\\d+}")
        re.compile(r"^/path/(?P<project>[\\w_.-]+)/(?P<episode>ep\\d+)$")

    :param pattern: String representing a template pattern path,
        with or without tokens.

    :param default_expression: Regular expression pattern to use for tokens
        when no expression is specified. Default is
        :data:`nomanclator.symbol.DEFAULT_TOKEN_EXPRESSION`.

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


def generate_scene_name(pattern, suffix, append_username=False, token_mapping=None):
    """Generate scene name from *pattern* using a mapping of resolved tokens.

    :param pattern: String representing a template base,
        with or without tokens.

    :param suffix: Suffix to apply for the generated name (e.g. "nk" or "hrox").

    :param append_username: Indicate whether username should be appended to base name.
        Default is False.

    :param token_mapping: Mapping regrouping resolved token values associated
        with their name. Default is None.

    :return: String name.

    :raise: exc:`ValueError` if a token within the *pattern* does not have any
        value within the token map.

    """
    if append_username:
        pattern += "_{username}"

    pattern += ".{}".format(suffix)
    return resolve(pattern, token_mapping or {})


def generate_output_name(
    pattern, suffix, append_passname_to_subfolder=False, append_passname=False,
    append_colorspace=False, append_username=False, multi_views=False, token_mapping=None
):
    """Generate output name from *pattern* using a mapping of resolved tokens.

    :param pattern: String representing a template base,
        with or without tokens.

    :param suffix: Suffix to apply for the generated name (e.g. "exr").

    :param append_passname_to_subfolder: Indicate whether passname should be appended to sub-folder.
        Default is False.

    :param append_passname: Indicate whether passname should be appended to base name.
        Default is False.

    :param append_colorspace: Indicate whether colorspace should be appended to base name.
        Default is False.

    :param append_username: Indicate whether username should be appended to base name.
        Default is False.

    :param multi_views: Indicate whether the view should be appended to base name
        with the pattern '%V'. Default is False.

    :param token_mapping: Mapping regrouping resolved token values associated
        with their name. Default is None.

    :return: String name.

    :raise: exc:`ValueError` if a token within the *pattern* does not have any
        value within the token map.

    """
    elements = pattern.split(os.sep)
    if len(elements) > 1 and append_passname_to_subfolder:
        elements[-2] += "_{passname}"

    if append_colorspace:
        elements[-1] += "_{colorspace}"

    if append_username:
        elements[-1] += "_{username}"

    if append_passname:
        elements[-1] += "_{passname}"

    if multi_views:
        elements[-1] += "_%V"

    if suffix not in VIDEO_TYPES:
        elements[-1] += ".{padding}"

    elements[-1] += ".{}".format(suffix)
    return resolve(os.sep.join(elements), token_mapping or {})


def resolve(pattern, token_mapping):
    """Return the resolved name for *pattern*.

    :param pattern: String representing a template pattern,
        with or without tokens.

    :param token_mapping: Mapping regrouping resolved token values associated
        with their name.

    :return: String name.

    :raise: exc:`ValueError` if a token within the *pattern* does not have any
        value within the token map.

    """
    def _remove_expression(match):
        """Return corresponding pattern without expression."""
        return "{{{0}}}".format(match.group("name").split(":", 1)[0])

    sub_pattern = r"{(?P<name>.+?)}"
    pattern = re.sub(sub_pattern, _remove_expression, pattern)

    try:
        return pattern.format(**token_mapping)
    except KeyError as error:
        raise ValueError("Missing token value: {}".format(error))
