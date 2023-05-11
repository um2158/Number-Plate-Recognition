import setuptools

VERSION = '0.0.1'
PROJECT_NAME = 'Number Plate Recognition'
AUTHOR_NAME = 'Uday Mukhija'
DESCRIPTION = ' This is a  Number Plate Recognition Project'

setuptools.setup(
    version=VERSION,
    PROJECT_NAME = PROJECT_NAME,
    author= AUTHOR_NAME,
    description= DESCRIPTION,
    package_dir= {"":"src"},
    packages= setuptools.find_packages(where='src')
)