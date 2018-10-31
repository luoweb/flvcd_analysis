#!/usr/bin/env python

from setuptools import setup, find_packages

version='0.1'
readme = open('README.md', 'r').read()

setup(
    name='flvcd_client',
    version=version,
    description='use flvcd to download video',
    long_description=readme + '\n\n',
    author='lsl',
    author_email='lin.sl.0001@gmail.com',
    license='MIT',
    zip_safe=False,
    packages = ['flvcd_client'],
    install_requires=['bs4', 'tqdm'],
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ),
    entry_points={'console_scripts':['flvcd_client = flvcd_client:main']},
)
