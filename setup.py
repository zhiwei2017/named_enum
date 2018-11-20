from setuptools import setup, find_packages
import os


source_path = 'src'
# Load README as description of package
with open('README.md') as readme_file:
    long_description = readme_file.read()

# Get current version
with open(os.path.join('VERSION')) as version_file:
    version = version_file.read().strip()

setup(
    name='named_enum',
    version=version,
    author='KnightConan',
    author_email='7a6869776569@gmail.com',
    description='Named Enumeration',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/KnightConan/sspdatatables',
    packages=find_packages(source_path),
    package_dir={'': source_path},
    include_package_data=True,
    install_requires = [
    ],
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
