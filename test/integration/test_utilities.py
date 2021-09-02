# -*- coding: utf-8 -*-

import os

import pytest


@pytest.fixture()
def scene_path(temporary_directory):
    """Return mocked scene path names."""
    names = [
        "project1_sh001_v001_steve.nk",
        "project2_sh002_comp_v001.nk",
        "project2_sh002_precomp_v001.nk",
        "project2_sh002_precomp_v002.nk",
        "project2_sh003_comp_v001.nk",
        "project2_sh003_comp_v002_steve.nk",
        "project2_sh003_comp_vINCORRECT.nk",
    ]

    for name in names:
        path = os.path.join(temporary_directory, name)

        with open(path, "w") as stream:
            stream.write("")

    return temporary_directory


def test_fetch_next_version_unmatched(scene_path):
    """Return version 1 when no files are matching."""
    import nomenclator.utilities

    pattern = "{project}_{shot}_{description}_v{version}"

    token_mapping = {
        "project": "project3",
        "shot": "sh001",
        "description": "comp",
    }
    version = nomenclator.utilities.fetch_next_version(
        scene_path, pattern, token_mapping
    )
    assert version == 1


def test_fetch_next_version_unmatched_tokens(scene_path):
    """Return version 1 when no files are matching with incoming tokens."""
    import nomenclator.utilities

    pattern = "{project}_{shot}_{description}_v{version}"

    token_mapping = {
        "project": "project1",
        "shot": "sh001",
        "description": "comp",
    }
    version = nomenclator.utilities.fetch_next_version(
        scene_path, pattern, token_mapping
    )
    assert version == 1


def test_fetch_next_version_one_match(scene_path):
    """Return version 2 when one file is matching with version 1."""
    import nomenclator.utilities

    pattern = "{project}_{shot}_{description}_v{version}"

    token_mapping = {
        "project": "project2",
        "shot": "sh002",
        "description": "comp",
    }
    version = nomenclator.utilities.fetch_next_version(
        scene_path, pattern, token_mapping
    )
    assert version == 2


def test_fetch_next_version_two_match(scene_path):
    """Return version 3 when two files are matching and latest version is 2."""
    import nomenclator.utilities

    pattern = "{project}_{shot}_{description}_v{version}"

    token_mapping = {
        "project": "project2",
        "shot": "sh002",
        "description": "precomp",
    }
    version = nomenclator.utilities.fetch_next_version(
        scene_path, pattern, token_mapping
    )
    assert version == 3


def test_fetch_next_version_two_match_with_options(scene_path):
    """Same scenario as previous test with username appended to latest file."""
    import nomenclator.utilities

    pattern = "{project}_{shot}_{description}_v{version}"

    token_mapping = {
        "project": "project2",
        "shot": "sh003",
        "description": "comp",
    }
    version = nomenclator.utilities.fetch_next_version(
        scene_path, pattern, token_mapping
    )
    assert version == 3


def test_fetch_template_config_matching():
    """Return matching template configuration."""
    import nomenclator.utilities
    from nomenclator.config import TemplateConfig

    path = "/path/my_project/ep002/sh004/scripts"

    config = TemplateConfig(
        id="Config",
        pattern_path=r"/path/{project}/{episode:ep\d+}/{shot:sh\d+}/scripts",
        pattern_base=r"{project}_{episode}_{shot}_v{version}.nk",
        default_expression=r"[\w_.-]+",
        match_start=True,
        match_end=True,
        outputs=None,
    )

    token_mapping = {}

    result = nomenclator.utilities.fetch_template_config(
        path, [config], token_mapping
    )
    assert result == config
    assert token_mapping == {
        "project": "my_project",
        "episode": "ep002",
        "shot": "sh004",
    }


def test_fetch_template_config_unmatched():
    """Fail to match config when shot does not match given expression."""
    import nomenclator.utilities
    from nomenclator.config import TemplateConfig

    path = "/path/my_project/ep002/sh004_SPECIAL/scripts"

    config = TemplateConfig(
        id="Config",
        pattern_path=r"/path/{project}/{episode:ep\d+}/{shot:sh\d+}/scripts",
        pattern_base=r"{project}_{episode}_{shot}_v{version}.nk",
        default_expression=r"[\w_.-]+",
        match_start=True,
        match_end=True,
        outputs=None,
    )

    token_mapping = {}

    result = nomenclator.utilities.fetch_template_config(
        path, [config], token_mapping
    )
    assert result is None
    assert token_mapping == {}


def test_fetch_template_config_unmatched_end():
    """Fail to match config when path must match end of pattern."""
    import nomenclator.utilities
    from nomenclator.config import TemplateConfig

    path = "/path/my_project/ep002/sh004/scripts/subfolder"

    config = TemplateConfig(
        id="Config",
        pattern_path=r"/path/{project}/{episode:ep\d+}/{shot:sh\d+}/scripts",
        pattern_base=r"{project}_{episode}_{shot}_v{version}.nk",
        default_expression=r"[\w_.-]+",
        match_start=True,
        match_end=True,
        outputs=None,
    )

    token_mapping = {}

    result = nomenclator.utilities.fetch_template_config(
        path, [config], token_mapping
    )
    assert result is None
    assert token_mapping == {}


def test_fetch_template_config_match_flexible_end():
    """Same scenario as previous test but with flexible end anchor."""
    import nomenclator.utilities
    from nomenclator.config import TemplateConfig

    path = "/path/my_project/ep002/sh004/scripts/subfolder"

    config = TemplateConfig(
        id="Config",
        pattern_path=r"/path/{project}/{episode:ep\d+}/{shot:sh\d+}/scripts",
        pattern_base=r"{project}_{episode}_{shot}_v{version}.nk",
        default_expression=r"[\w_.-]+",
        match_start=True,
        match_end=False,
        outputs=None,
    )

    token_mapping = {}

    result = nomenclator.utilities.fetch_template_config(
        path, [config], token_mapping
    )
    assert result == config
    assert token_mapping == {
        "project": "my_project",
        "episode": "ep002",
        "shot": "sh004",
    }


def test_fetch_template_config_unmatched_start():
    """Fail to match config when path must match start of pattern."""
    import nomenclator.utilities
    from nomenclator.config import TemplateConfig

    path = "/root/path/my_project/ep002/sh004/scripts"

    config = TemplateConfig(
        id="Config",
        pattern_path=r"/path/{project}/{episode:ep\d+}/{shot:sh\d+}/scripts",
        pattern_base=r"{project}_{episode}_{shot}_v{version}.nk",
        default_expression=r"[\w_.-]+",
        match_start=True,
        match_end=True,
        outputs=None,
    )

    token_mapping = {}

    result = nomenclator.utilities.fetch_template_config(
        path, [config], token_mapping
    )
    assert result is None
    assert token_mapping == {}


def test_fetch_template_config_match_flexible_start():
    """Same scenario as previous test but with flexible start anchor."""
    import nomenclator.utilities
    from nomenclator.config import TemplateConfig

    path = "/root/path/my_project/ep002/sh004/scripts"

    config = TemplateConfig(
        id="Config",
        pattern_path=r"/path/{project}/{episode:ep\d+}/{shot:sh\d+}/scripts",
        pattern_base=r"{project}_{episode}_{shot}_v{version}.nk",
        default_expression=r"[\w_.-]+",
        match_start=False,
        match_end=True,
        outputs=None,
    )

    token_mapping = {}

    result = nomenclator.utilities.fetch_template_config(
        path, [config], token_mapping
    )
    assert result == config
    assert token_mapping == {
        "project": "my_project",
        "episode": "ep002",
        "shot": "sh004",
    }
