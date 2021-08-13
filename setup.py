# -*- coding: utf-8 -*-

import os
import re

from setuptools import setup, find_packages

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
SOURCE_PATH = os.path.join(ROOT_PATH, "source")
README_PATH = os.path.join(ROOT_PATH, "README.rst")

PACKAGE_NAME = "nomenclator"

# Read version from source.
with open(
    os.path.join(SOURCE_PATH, PACKAGE_NAME, "_version.py")
) as _version_file:
    VERSION = re.match(
        r".*__version__ = \"(.*?)\"", _version_file.read(), re.DOTALL
    ).group(1)

# Compute dependencies.
DOC_REQUIRES = [
    "sphinx >= 1.8, < 2",
    "sphinx_rtd_theme >= 0.1.6, < 1",
    "lowdown >= 0.2.0, < 2"
]

TEST_REQUIRES = [
    "pytest-runner >= 2.7, < 3",
    "pytest >= 4, < 5",
    "pytest-mock >= 1.2, < 2",
    "pytest-xdist >= 1.18, < 2",
    "pytest-cov >= 2, < 3",
]

# Execute setup.
setup(
    name="nomenclator-nuke",
    version=VERSION,
    description="Nuke plugin to name script and render outputs",
    long_description=open(README_PATH).read(),
    url="https://github.com/buddly27/nomenclator-nuke",
    keywords=["nuke", "foundry"],
    author="Jeremy Retailleau",
    packages=find_packages(SOURCE_PATH),
    package_dir={
        "": "source"
    },
    include_package_data=True,
    python_requires=(
        ">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5*"
    ),
    install_requires=[],
    tests_require=TEST_REQUIRES,
    extras_require={
        "doc": DOC_REQUIRES,
        "test": TEST_REQUIRES,
        "dev": DOC_REQUIRES + TEST_REQUIRES
    },
    zip_safe=False,
    classifiers=[
        "Environment :: Plugins",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Utilities",
    ]
)
