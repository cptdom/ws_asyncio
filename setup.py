from setuptools import setup, find_packages
from exchange.version import __version__, APP_NAME

try:
    with open('README.md', 'r') as fh:
        long_description = fh.read()
except FileNotFoundError:
    long_description = 'README.md not found'

try:
    with open('requirements.txt') as fh:
        required = fh.read().splitlines()
except FileNotFoundError:
    required = []

setup(
    name=APP_NAME,
    version=__version__,
    author='cptdom',
    author_email='hartdom97@gmail.com',
    description='Ematiq assignment solution',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='',
    include_package_data=True,
    zip_safe=False,
    packages=find_packages(),
    install_requires=required,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    entry_points={
        'console_scripts': ['exchange=exchange.main:main'],
    })
