import pathlib
from setuptools import setup, find_packages

from pysgrs import __version__

_PATH = pathlib.Path(__file__).resolve().parents[0]
_PACKAGE = _PATH.parts[-1]

with (_PATH/'requirements.txt').open() as fh:
    reqs = fh.read().splitlines()

setup(
    name=_PACKAGE,
    version=__version__,
    url='https://github.com/jlandercy/{package:}'.format(package=_PACKAGE),
    license='GPL v.3',
    author='Jean Landercy',
    author_email='jeanlandercy@live.com',
    description='Minimal Python 3 Package',

    packages=find_packages(exclude=[]),
    package_data={
       _PACKAGE: [
           'resources/*.json',
           'resources/books/**/*.txt',
           'resources/notebooks/*.ipynb',
           'toolbox/resources/*.json'
       ]
    },
    scripts=[],
    python_requires='>=3.7',
    install_requires=reqs,
    classifiers=[
         "Intended Audience :: Science/Research",
         "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
         "Operating System :: OS Independent",
         "Topic :: Scientific/Engineering",
    ],
    entry_points={
        'console_scripts': ['{package:}={package:}.run:main'.format(package=_PACKAGE)]
    },
    zip_safe=False,
)
