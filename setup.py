from setuptools import find_packages, setup
import os

from libloader import __author__, __author_email__, __doc__, __version__

# Read the long description from README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="libloader",
    version=__version__,
    author=__author__,
    author_email=__author_email__,
    description=__doc__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    zip_safe=False,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.6",
)
