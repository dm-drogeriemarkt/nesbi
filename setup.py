#!/usr/bin/env python
import uuid

try:
    from setuptools import find_packages, setup
except ImportError:
    from distutils.core import setup

try:  # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError:  # for pip <= 9.0.3
    from pip.req import parse_requirements

install_reqs = parse_requirements('requirements.txt', session=uuid.uuid1())
reqs = [str(ir.req) for ir in install_reqs]


__author__ = "Simon Metzger"
__author_email__ = "simon.metzger@dm.de"
__license__ = "MIT License"

__version__ = "1.0.3"

setup(name="nesbi",
      version=__version__,
      description="Nesbi (Network Scan, Build and Import data)",
      author=__author__,
      author_email=__author_email__,
      url='https://github.com/dm-drogeriemarkt/nesbi',
      include_package_data=True,
      install_requires=reqs,
      packages=find_packages(exclude=("test*", )),
      license=__license__,
      test_suite="tests",
      platforms="any",
      classifiers=["Development Status :: 4 - Beta",
                   "Programming Language :: Python :: 3",
                   "Programming Language :: Python :: 3 :: Only",
                   "Programming Language :: Python :: 3.6",
                   "License :: OSI Approved :: MIT License"
                   ])
