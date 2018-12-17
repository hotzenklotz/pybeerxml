from setuptools import setup
from setuptools.command.test import test as TestCommand
from setuptools.command.install import install
import sys
import os

import pybeerxml

# circleci.py version
VERSION = "1.0.5"

def readme():
    """print long description"""
    with open('README.md') as f:
        return f.read()


class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches our version"""
    description = 'verify that the git tag matches our version'

    def run(self):
        tag = os.getenv('CIRCLE_TAG')

        if tag != VERSION:
            info = "Git tag: {0} does not match the version of this app: {1}".format(
                tag, VERSION
            )
            sys.exit(info)

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ["--junitxml=test-reports/pytest/junit.xml"]
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)

setup(
    name = 'pybeerxml',
    packages = ['pybeerxml'],
    version = VERSION,
    description = 'A BeerXML Parser',
    long_description=readme(),
    long_description_content_type="text/markdown",
    author = 'Tom Herold',
    author_email = 'heroldtom@gmail.com',
    url = 'https://github.com/hotzenklotz/pybeerxml',
    download_url = 'https://github.com/hotzenklotz/pybeerxml/tarball/{}'.format(VERSION),
    tests_require=['pytest'],
    cmdclass={
        'test': PyTest,
        'verify': VerifyVersionCommand
    },
    platforms='any',
    keywords = ['beerxml', 'beer', 'xml', 'brewing'],
    classifiers = [
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    license='MIT',
    extras_require={
          'testing': ['pytest'],
      }
)
