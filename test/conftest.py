# -*- coding: utf-8 -*-

import os
import shutil
import sys
import tempfile

import pytest


@pytest.fixture()
def temporary_file(request):
    """Return a temporary file path."""
    file_handle, path = tempfile.mkstemp()
    os.close(file_handle)

    def cleanup():
        """Remove temporary file."""
        try:
            os.remove(path)
        except OSError:
            pass

    request.addfinalizer(cleanup)
    return path


@pytest.fixture()
def temporary_directory(request):
    """Return a temporary directory path."""
    path = tempfile.mkdtemp()

    def cleanup():
        """Remove temporary directory."""
        shutil.rmtree(path)

    request.addfinalizer(cleanup)

    return path


@pytest.fixture(autouse=True)
def nuke_mocker(mocker):
    """Mock the Nuke Python API."""
    mocker.patch.dict(sys.modules, {"nuke": mocker.MagicMock()})


@pytest.fixture(autouse=True)
def hiero_mocker(mocker):
    """Mock the Hiero Python API."""
    mocker.patch.dict(
        sys.modules, {
            "hiero": mocker.MagicMock(),
            "hiero.core": mocker.MagicMock(),
        }
    )


@pytest.fixture(autouse=True)
def qt_mocker(mocker):
    """Mock the Qt library."""
    mocker.patch.dict(sys.modules, {"nomenclator.vendor.Qt": mocker.MagicMock()})
