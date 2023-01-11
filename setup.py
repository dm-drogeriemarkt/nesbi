#!/usr/bin/env python
from setuptools import find_packages, setup


__author__ = "Simon Metzger"
__author_email__ = "simon.metzger@dm.de"
__license__ = "MIT License"

__version__ = "1.0.5"

setup(name="nesbi",
      version=__version__,
      description="Nesbi (Network Scan, Build and Import data)",
      author=__author__,
      author_email=__author_email__,
      url='https://github.com/dm-drogeriemarkt/nesbi',
      include_package_data=True,
      packages=find_packages(exclude=("test*", )),
      license=__license__,
      test_suite="tests",
      platforms="any",
      classifiers=["Development Status :: 4 - Beta",
                   "Programming Language :: Python :: 3",
                   "Programming Language :: Python :: 3 :: Only",
                   "Programming Language :: Python :: 3.8",
                   "Programming Language :: Python :: 3.9",
                   "License :: OSI Approved :: MIT License"
                   ])
