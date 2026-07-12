#!/usr/bin/env python3

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="teletext",
    version="0.0.8",
    author="Zsombor Kalmar",
    description="Desktop version of some Teletext services.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    project_urls={
        "GitHub": "https://github.com/zsobix/teletext",
        "PyPI": "https://pypi.org/project/teletext/",
    },
    license="GPLv3",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Natural Language :: English",
        "Operating System :: POSIX",
        "Operating System :: MacOS",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.14",
    ],
    platforms="any",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=[
        "requests >= 2.34.2",
        "beautifulsoup4 >= 4.15.0"
    ],
    entry_points={
        "console_scripts": [
            "teletext = teletext.__main__:main",
        ]
    },
)
