#! /usr/bin/env python3

"""
Package setup file
"""

from setuptools import find_packages, setup

with open("README.md") as fi:
    long_description = fi.read()

packages = find_packages()

setup(
    name="f1-2020-telemetry",
    version="0.2.1",
    author="Guillaume Parent",
    author_email="gp@gparent.net",
    description="A package to handle UDP telemetry data as sent by the F1 2020 game.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/f1-2020-telemetry/",
    project_urls={
        "Documentation": "https://f1-2020-telemetry.readthedocs.io/en/latest/",
        "Source Repository": "https://gitlab.com/gparent/f1-2020-telemetry/",
    },
    packages=packages,
    entry_points={
        "console_scripts": [
            "f1-2020-telemetry-recorder=f1_2020_telemetry.cli.recorder:main",
            "f1-2020-telemetry-player=f1_2020_telemetry.cli.player:main",
            "f1-2020-telemetry-monitor=f1_2020_telemetry.cli.monitor:main",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Topic :: Games/Entertainment",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
