"""Builds boilerplate as a package

"""
import setuptools
from distutils import util

version = dict()
path = util.convert_path("src/zucced_api/core/version.py")
with open(path) as file:
    exec(file.read(), version)

setuptools.setup(version=version["__version__"])
