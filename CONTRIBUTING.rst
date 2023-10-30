Contributing
============

Any contributions are welcome and appreciated!

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/zhiwei2017/named_enum/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with **bug** and **help wanted** is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the issues for features. Anything tagged with **enhancement**
and **help wanted** is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

Named Enum could always use more documentation, whether as part of the
official Named Enum docs, in docstrings, or even on the web in blog posts,
articles, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/zhiwei2017/named_enum/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.

Get Started!
------------

Ready to contribute? Here's how to set up `named_enum` for local development.

1. Fork the `named_enum` repo on GitHub.
2. Clone your fork locally::

    $ git clone git@your_repo_url.git

3. Install your local copy into a virtualenv. Assuming you have virtualenv installed, this is how you set up your fork for local development::

    $ python -m virtualenv named_enum-venv
    $ source named_enum-venv/bin/activate
    $ cd named_enum/

   Now you can install `named_enum` in develop mode in your virtual environment::

    $ pip install -e .

   or::

    $ poetry install

4. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

5. When you're done making changes, check that your changes pass all linting checks and the
   tests, including testing other Python versions with tox::

    $ make install
    $ make flake8
    $ make mypy
    $ make bandit
    $ make test
    $ tox

6. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

7. Submit a pull request through the GitHub website.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.
3. The pull request should work for Python 3.7, 3.8, 3.9, 3.10, 3.11, 3.12.

Deploying
---------

To deploy the package, just run::

    $ poetry version patch  # possible: major / minor / patch / premajor / preminor / prepatch
    $ git commit -m "Bump version: {old_version} -> {new_version}."
    $ git push
    $ git push --tags

Github Actions will do the rest.