from setuptools import setup, find_packages

setup(
    name='project0',
    version='1.0',
    author='Rama Satyanarayamna Murthy Reddy Velagala',
    author_email='r.velagala@ufl.edu', 
    packages=find_packages(exclude=('tests', 'docs', 'resources')),
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)

