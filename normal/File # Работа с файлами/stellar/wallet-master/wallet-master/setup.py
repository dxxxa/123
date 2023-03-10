# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages
from codecs import open
from os import path
import re

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()


def load_version():
    version_file = "pywallet/_version.py"
    version_line = open(version_file).read().rstrip()
    vre = re.compile(r'__version__ = "([^"]+)"')
    matches = vre.findall(version_line)

    if matches and len(matches) > 0:
        return matches[0]
    else:
        raise RuntimeError(
            "Cannot find version string in {version_file}.".format(
                version_file=version_file))


version = load_version()

setup(
    name='Wallet',
    version=version,
    description='Wallet for BuyWithTokens.org',
    long_description=readme,
    author='Arnon Hongklay',
    author_email='arnon@hongklay.com',
    url='https://github.com/arnonhongklay/wallet',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=[
        'base58>=0.2.2',
        'ecdsa>=0.11',
        'six>=1.8.0',
        'two1>=3.10.8',
        'pycryptodome>=3.6.6',
    ]
)
