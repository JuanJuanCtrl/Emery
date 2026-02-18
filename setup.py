#!/usr/bin/env python3
"""Setup script for Emery CLI."""

from setuptools import setup, find_packages

setup(
    name="emery-cli",
    version="1.0.0",
    description="Modern file upload CLI with drag-and-drop support",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Emery Team",
    author_email="cli@emery.local",
    url="https://github.com/JuanJuanCtrl/Emery",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "typer>=0.9.0",
        "rich>=13.7.0",
        "GitPython>=3.1.40",
        "click>=8.1.7",
    ],
    entry_points={
        "console_scripts": [
            "emery=emery_cli.main:main",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
