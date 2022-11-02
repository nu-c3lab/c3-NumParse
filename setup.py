from setuptools import setup, find_packages

with open('requirements.txt', 'r') as requirements:
    install_requires = requirements.read().splitlines()

setup(
    name='NumParse',
    version='0.1.0',
    author='C3 Lab',
    author_email='markosterbentz2023@u.northwestern.edu',
    description='A package for extracting numeric values/ranges from strings.',
    url='https://github.com/nu-c3lab/c3-NumParse',
    packages=find_packages(),
    python_requires='>=3.7',
    install_requires= install_requires,
    include_package_data=True
    )
