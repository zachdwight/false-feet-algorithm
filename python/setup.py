"""Setup configuration for False Feet Algorithm package."""

from setuptools import setup, find_packages
import os

# Read README
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="false-feet-algorithm",
    version="0.1.0",
    author="Zach Dwight",
    author_email="",  # Add your email here if publishing
    description="A novel multi-branch hypothesis evaluation system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zachdwight/false-feet-algorithm",
    project_urls={
        "Bug Tracker": "https://github.com/zachdwight/false-feet-algorithm/issues",
        "Documentation": "https://github.com/zachdwight/false-feet-algorithm",
        "Source Code": "https://github.com/zachdwight/false-feet-algorithm",
    },
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.7",
    extras_require={
        "viz": ["matplotlib>=3.3.0"],
        "dev": ["pytest>=6.0", "pytest-cov>=2.10.0", "black>=21.0", "mypy>=0.900", "tox>=3.0"],
    },
)
