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


def test_fetch_next_version(scene_path):
    """Fetch next version from scene files."""
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

    token_mapping = {
        "project": "project2",
        "shot": "sh002",
        "description": "comp",
    }
    version = nomenclator.utilities.fetch_next_version(
        scene_path, pattern, token_mapping
    )
    assert version == 2

    token_mapping = {
        "project": "project2",
        "shot": "sh002",
        "description": "precomp",
    }
    version = nomenclator.utilities.fetch_next_version(
        scene_path, pattern, token_mapping
    )
    assert version == 3

    token_mapping = {
        "project": "project2",
        "shot": "sh003",
        "description": "comp",
    }
    version = nomenclator.utilities.fetch_next_version(
        scene_path, pattern, token_mapping
    )
    assert version == 3

    token_mapping = {
        "project": "project3",
        "shot": "sh001",
        "description": "comp",
    }
    version = nomenclator.utilities.fetch_next_version(
        scene_path, pattern, token_mapping
    )
    assert version == 1
