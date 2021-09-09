Release Notes
=============

Versioning
----------

Describe how the project is versioned. For example:

We use `SemVer <http://semver.org/>`_ for versioning. For the versions available, see the `the project tags <https://gitlab.com/your/project/tags>`_.

`v1.0.1 <https://github.com/KnightConan/named_enum/releases/tag/v1.0.1>`_
-------------------------------------------------------------------------

*Features/Bug Fixes:*

* new feature for python 3.8, support enum item name check
* refactor tests to reduce code duplications
* use github actions to replace external CIs
* remove pytest-mock from test-requirements and use unittest.mock replace its usages in tests

`v1.0.2 <https://github.com/KnightConan/named_enum/releases/tag/v1.0.2>`_
-------------------------------------------------------------------------

*Features/Bug Fixes:*

* Introduces `#64 <https://github.com/KnightConan/named_enum/pull/64>`_: Disable pyup checks for test-requirements
* Introduces `#65 <https://github.com/KnightConan/named_enum/pull/65>`_:

    * remove irrelevant badge
    * add badge for sonarcloud
    * fix issues in tests found by sonarcloud

* Closed `#66 <https://github.com/KnightConan/named_enum/issues/66>`_:  the package is incompatible with python 3.8+ through `#67 <https://github.com/KnightConan/named_enum/pull/67>`_
