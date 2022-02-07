from setuptools import setup, find_packages

with open('requirements.txt', 'r') as requirements:
    install_requires = requirements.read().splitlines()

setup(
    name='c3-NumParse',
    version='0.0.2',
    author='C3 Lab',
    author_email='markosterbentz2023@u.northwestern.edu',
    description='A package for performing numeric parsing.',
    url='https://github.com/nu-c3lab/c3-NumParse',
    packages=find_packages(),
    python_requires='>=3.7',
    install_requires= install_requires,
    include_package_data=True
    )