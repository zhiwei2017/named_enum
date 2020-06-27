import os
import distutils.text_file
from pathlib import Path
from typing import List
from setuptools import setup


# Load README as description of package
with open('README.rst') as readme_file:
    long_description = readme_file.read()

# Get current version
with open(os.path.join('VERSION')) as version_file:
    version = version_file.read().strip()


def _parse_requirements(filename: str) -> List[str]:
    """Return requirements from requirements file."""
    return distutils.text_file.TextFile(filename=str(Path(__file__).with_name(filename))).readlines()


setup(
    name='named_enum',
    version=version,
    author='Zhiwei Zhang',
    author_email='zhiwei2017@gmail.com',
    description='Named Enumeration',
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url='https://github.com/KnightConan/named_enum',
    license='MIT License',
    packages=["named_enum"],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation",
        "Topic :: Utilities",
        "Natural Language :: English",
        "Intended Audience :: Developers",
    ],
    setup_requires=["pytest-runner"],
    tests_require=_parse_requirements('test-requirements.txt'),
)
