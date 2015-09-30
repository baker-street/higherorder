# -*- coding: utf-8 -*-
"""
higherorder  Copyright (C) 2015  Steven Cutting - License GPLv3: higherorder/LICENSE
"""

from higherorder import(__title__, __version__, __status__)


from setuptools import setup, find_packages

with open("README.md") as fp:
    THE_LONG_DESCRIPTION = fp.read()

TESTDEPEND = ['pytest']
# DEVDEPEND = []
# Work on making python-magic optional.
FULLDEPEND = []
FULLDEPEND.extend(TESTDEPEND)

setup(name=__title__,
      version=__version__,
      license='GNU AGPL',
      description="Functional style tools used for composition of functions.",
      long_description=THE_LONG_DESCRIPTION,
      classifiers=['Topic :: functional',
                   'Intended Audience :: Developers',
                   'Operating System :: GNU Linux',
                   'Operating System :: OSX :: MacOS :: MacOS X',
                   'Operating System :: POSIX',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3.4',
                   'License :: GNU AGPL',
                   'Copyright :: higherorder  Copyright (C) 2015  Steven Cutting',
                   'Status :: ' + __status__,
                   ],
      keywords='functional, tools, composition, functions, transducer',
      author='Steven Cutting',
      author_email='steven.e.cutting@linux.com',
      packages=find_packages(exclude=('scripts', 'tests')),
      # zip_safe=False,
      install_requires=[
                        ],
      extras_require={
          # 'dev': DEVDEPEND,
          'full': FULLDEPEND,
          'test': TESTDEPEND,
      }
      )
