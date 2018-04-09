#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name='magic-elo',
    version='0.1',
    description='ELO tool for Magic',
    author='Louis Aumaitre',
    packages=find_packages(),
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    install_requires=[
    ],
    include_package_data=True,
    zip_safe=False,
)
