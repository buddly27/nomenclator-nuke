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


def test_fetch_next_version_scenario1(scene_path):
    """Fetch next version from scene paths.

    No scene file is matching the incoming pattern. Therefore we
    expect version 1 to be returned.

    """
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


def test_fetch_next_version_scenario2(scene_path):
    """Fetch next version from scene paths.

    No scene file is matching the incoming pattern with resolved tokens
    provided. Therefore we expect version 1 to be returned.

    """
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


def test_fetch_next_version_scenario3(scene_path):
    """Fetch next version from scene paths.

    One scene file is matching the incoming pattern:

    * project2_sh002_comp_v001.nk

    As the version detected on this file is '1', we expect version 2
    to be returned.

    """
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


def test_fetch_next_version_scenario4(scene_path):
    """Fetch next version from scene paths.

    Two scene files are matching the incoming pattern:

    * project2_sh002_precomp_v001.nk
    * project2_sh002_precomp_v002.nk

    As the latest version detected on these files is '2', we expect
    version 3 to be returned.

    """
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


def test_fetch_next_version_scenario5(scene_path):
    """Fetch next version from scene paths.

    Like in scenario 4, Two scene files are matching the
    incoming pattern:

    * project2_sh003_comp_v001.nk
    * project2_sh003_comp_v002_steve.nk

    As the latest version detected on these files is '2', we expect
    version 3 to be returned.

    """
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


def test_fetch_template_config_scenario1():
    """Return template configuration compatible.

    One of the incoming configurations is matching with incoming path.

    """
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
        append_username_to_name=True,
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


def test_fetch_template_config_scenario2():
    """Return template configuration compatible.

    None of the incoming configurations is matching with incoming path.

    """
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
        append_username_to_name=True,
        outputs=None,
    )

    token_mapping = {}

    result = nomenclator.utilities.fetch_template_config(
        path, [config], token_mapping
    )
    assert result is None
    assert token_mapping == {}


def test_fetch_template_config_scenario3():
    """Return template configuration compatible.

    Incoming path is not matching pattern exactly as it contains an
    additional subfolder. Therefore, no config will be returned

    """
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
        append_username_to_name=True,
        outputs=None,
    )

    token_mapping = {}

    result = nomenclator.utilities.fetch_template_config(
        path, [config], token_mapping
    )
    assert result is None
    assert token_mapping == {}


def test_fetch_template_config_scenario4():
    """Return template configuration compatible.

    Like the scenario 3, incoming path is not matching pattern exactly
    as it contains an additional subfolder. However, the 'match_end'
    option is set to False, so it is still compatible. Therefore, the
    config will be returned.

    """
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
        append_username_to_name=True,
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


def test_fetch_template_config_scenario5():
    """Return template configuration compatible.

    Incoming path is not matching pattern exactly as it contains an
    additional root folder. Therefore, no config will be returned

    """
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
        append_username_to_name=True,
        outputs=None,
    )

    token_mapping = {}

    result = nomenclator.utilities.fetch_template_config(
        path, [config], token_mapping
    )
    assert result is None
    assert token_mapping == {}


def test_fetch_template_config_scenario6():
    """Return template configuration compatible.

    Like the scenario 5, incoming path is not matching pattern exactly
    as it contains an additional root folder. However, the 'match_start'
    option is set to False, so it is still compatible. Therefore, the
    config will be returned.

    """
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
        append_username_to_name=True,
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
