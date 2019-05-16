import os
from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='sports.py',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    version='2.0.5',
    description='A simple Python package to gather live sports scores',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    author='Evan Sloan',
    author_email='evansloan082@gmail.com',
    url='https://github.com/evansloan/sports.py',
    download_url='https://github.com/evansloan/sports.py/archive/v2.0.5.tar.gz',
    keywords=['sports', 'scores', 'live scores', 'hockey', 'basketball', 'baseball', 'football'],
    install_requires=['requests', 'bs4', 'defusedxml'],
    python_requires='>=3'
)
