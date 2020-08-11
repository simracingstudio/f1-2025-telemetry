#! /usr/bin/env python3

from setuptools import setup

with open("README.md") as fi:
    long_description=fi.read()

setup(

    name="f1-2020-telemetry",
    version="0.1.3",

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

    # Since we don't have __init__.py files, our packages aren't found by setuptools.find_packages().
    # We therefore specify them explicitly here.
    packages=['f1_2020_telemetry', 'f1_2020_telemetry.cli'],

    entry_points={
        'console_scripts': [
            'f1-2020-telemetry-recorder=f1_2020_telemetry.cli.recorder:main',
            'f1-2020-telemetry-player=f1_2020_telemetry.cli.player:main',
            'f1-2020-telemetry-monitor=f1_2020_telemetry.cli.monitor:main'
        ]
    },

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Topic :: Games/Entertainment",
        "Operating System :: OS Independent"
    ],

    python_requires=">=3.6"
)
