import io

from setuptools import find_packages, setup

setup(
    name='bpm-projects-api',
    version='0.0.1',
    license='Copyright 2018 ioet Inc. All Rights Reserved.',
    maintainer='BPM Developers',
    description='API for managing projects in the BPM.',
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask>=1.0.2',
        'flask_restplus>=0.11.0',
        'Flask-Script>=2.0.6',
        'PyJWT',
    ],
    extras_require={
        'test': [
            'pytest',
            'coverage',
        ],
    },
)