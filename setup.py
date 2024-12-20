"""A setuptools based setup module.

See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""
from setuptools import find_packages, setup

setup(
    name="pyinsee",
    version="0.1.1",
    description="A package for collecting and processing company data from INSEE API",
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author="Ayman KUMA",
    author_email="aymankamel.mail@gmail.com",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        "requests",
        "python-dotenv",
    ],
    entry_points={
        'console_scripts': [
            'py-insee-setup=pyinsee.setup_cli:main',
            'py-insee=pyinsee.insee_cli:main',
        ],
    },
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)