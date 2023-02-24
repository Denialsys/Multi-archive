from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'For multiple compression and decompression'
LONG_DESCRIPTION = 'Package for programmatic archival or extraction of archive files with passwords'


setup(
    name="Multi-archive",
    version=VERSION,
    author="Denialsys (Jenver I.)",
    author_email="<denialsys@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['', '', ''],
    keywords=['python', 'zip', 'archive', '7zip'],
    classifiers=[
        "Development Status :: 2 - Developement",
        "Intended Audience :: ",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
    ]
)