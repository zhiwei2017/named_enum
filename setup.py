from setuptools import setup
import os


# Load README as description of package
with open('README.rst') as readme_file:
    long_description = readme_file.read()

# Get current version
with open(os.path.join('VERSION')) as version_file:
    version = version_file.read().strip()

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
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    setup_requires=["pytest-runner"],
    tests_require=['pytest'],
)
