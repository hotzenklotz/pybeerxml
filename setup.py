import sys
import os
from setuptools import setup
from setuptools.command.test import test as TestCommand
from setuptools.command.install import install

VERSION = "2.0.0"

def readme():
    """print long description"""
    with open("README.md") as file:
        return file.read()


class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches our version"""

    description = "verify that the git tag matches our version"

    def run(self):
        github_ref = os.getenv("GITHUB_REF") # should look like "refs/tags/v1.2.3"
        tag = github_ref.split("/")[-1]

        if tag != VERSION:
            info = "Git tag: {0} does not match the version of this app: {1}".format(
                tag, VERSION
            )
            sys.exit(info)

setup(
    name="pybeerxml",
    packages=["pybeerxml"],
    version=VERSION,
    description="A BeerXML Parser",
    long_description=readme(),
    long_description_content_type="text/markdown",
    author="Tom Herold",
    author_email="heroldtom@gmail.com",
    url="https://github.com/hotzenklotz/pybeerxml",
    download_url="https://github.com/hotzenklotz/pybeerxml/tarball/{}".format(VERSION),
    tests_require=["pytest"],
    cmdclass={"verify": VerifyVersionCommand},
    platforms="any",
    keywords=["beerxml", "beer", "xml", "brewing"],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    license="MIT",
    extras_require={
        "testing": ["pytest"],
    },
)
