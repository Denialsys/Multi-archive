from setuptools import setup, find_packages
import os


VERSION = '0.1.7'
DESCRIPTION = 'For multiple compression and decompression'
LONG_DESCRIPTION = 'Package for programmatic archival or extraction of archive files with passwords'


setup(
    name="Multi-archive",
    version=VERSION,
    author="Denialsys (Jenver I.)",
    author_email="<denialsys@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
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