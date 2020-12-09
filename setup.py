import pathlib
from setuptools import setup, find_packages

from pysgrs import __version__

path = pathlib.Path(__file__).resolve().parents[0]
package = path.parts[-1]

with (path / 'requirements.txt').open() as file_handler:
    requirements = file_handler.read().splitlines()

setup(
    name=package,
    version=__version__,
    url='https://github.com/jlandercy/{package:}'.format(package=package),
    license='BSD 3-Clause License',
    author='Jean Landercy',
    author_email='jeanlandercy@live.com',
    description='Pyhon SGRS Package',
    packages=find_packages(exclude=[]),
    package_data={
       package: [
            'resources/*.json',
            'resources/ngrams/**/*.json',
            'resources/books/**/*.txt',
            'resources/texts/**/*.txt',
            'resources/notebooks/*.ipynb'
       ]
    },
    scripts=[],
    python_requires='>=3.7',
    install_requires=requirements,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Natural Language :: French",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Topic :: Education",
        "Topic :: Games/Entertainment :: Puzzle Games",
        "Topic :: Security :: Cryptography",
        "Topic :: Software Development",
        "Topic :: Utilities"
    ],
    entry_points={
        'console_scripts': ['{package:}={package:}._new:main'.format(package=package)]
    },
    zip_safe=False,
)
