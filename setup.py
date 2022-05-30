#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" setup.py for cookiecutter-fastapi-sun-asterisk."""

from setuptools import setup

__version__ = "0.2.0"

with open("README.md") as readme_file:
    long_description = readme_file.read()

setup(
    name="cookiecutter-fastapi-sun-asterisk",
    version=__version__,
    description="A Cookiecutter template for creating FastAPI projects quickly.",
    long_description=long_description,
    author="Ha Hao Minh",
    author_email="ha.hao.minh@sun-asterisk.com",
    url="https://github.com/minhhh-0927/cookiecutter-fastapi-sun-asterisk",
    download_url="",
    packages=[],
    include_package_data=True,
    license="MIT",
    classifiers=[
        "Framework :: FastAPI",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development",
    ],
)