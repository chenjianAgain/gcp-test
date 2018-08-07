from setuptools import setup
from os import getenv


def get_name():
    base_name = 'gd-fenixlib'
    pyver = getenv('PYVER', '')
    pyver = pyver.replace('.', '', 1)
    versioning = "python{}-".format(pyver) if pyver else ''
    return '{0}{1}'.format(versioning, base_name)

def get_version():
    return getenv('MODULE_VERSION')

setup(
    name=get_name(),
    author='Workspace Email Infrastructure',
    author_email='emaildev@godaddy.com',
    version=get_version(),
    description='Shared library for fenix microservices',
    url='https://github.secureserver.net/EmailInfrastructure/fenixlib',
    packages=['fenixlib', 'fenixlib.clients', 'fenixlib.schemas', 'fenixlib.utils'],
    install_requires=[
        "requests",
        "zeep",
        "boto3"
    ]
)
