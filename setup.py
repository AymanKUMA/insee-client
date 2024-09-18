"""A setuptools based setup module.

See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""
from setuptools import find_packages, setup

setup(
    name="pyinsee",
    version="0.1.0",                  # Package version
    description="A package for collecting and processing \
          company data from INSEE API",
    author="Ayman KUMA",
    author_email="aymankamel.mail@example.com",
    packages=find_packages(),         # Automatically find and include all packages
    install_requires=[                # List of dependencies
        "requests",
        "python-dotenv",
    ],
    entry_points={
        'console_scripts': [
            'setup-cli=src.setup_cli:main',
            'insee-cli=src.insee_cli:main',
        ],
    },
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.8",          # Minimum Python version required
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)