"""Builds haveibeenzucced as a pip package."""
from distutils import util

import setuptools

version = {}
path = util.convert_path("src/zucced_api/core/version.py")
with open(path) as file:
    exec(file.read(), version)

setuptools.setup(version=version["__version__"])
