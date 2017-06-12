# Python Packaging

## Issues

 * Source often needs to be present to run a program.
 * For larger projects, this causes issues with versioning, sharing code between projects, documentation.
 * Git submodules don't work well with code review platforms, or versioning schemes.
 * Need a standard way to fetch external dependencies that works for both developers and users.
   * `pip install -re requirements.txt` is unsuitable for users as it often contains dependencies for unit tests.
 * Problems with references to internal packages often solved ad-hoc with `sys.path` or `PYTHONPATH`.

## History

There's a lot of historical background in this area:

 * [Python Packaging: Hate, hate, hate everywhere](http://lucumr.pocoo.org/2012/6/22/hate-hate-hate-everywhere/)
 * [Distribute is dead, use pip](http://stackoverflow.com/a/8550546)
 * [The current state (2015)](http://stackoverflow.com/a/30408520)
 * [Summary of Tools](http://stackoverflow.com/a/14753678)
 * [Python Packaging User Guide: Tool Recommendations](https://packaging.python.org/current/)

TL; DR: Use the latest version of `pip`.

## pip

 * Use `cookiecutter` to create templates for reproducibility.
 * Use a `setup.py` file, used by `pip` to manage the package.
 * For _users_, avoid git clones and submodules, instead use `pip` to obtain a directly importable package from a git repository. All dependencies will be automatically fulfilled.
 * For _developers_, clone the application from git then use `pip --editable` to make changes. This allows `pip` to install any packages defined by the program to be seen as if they were installed, matching the user's environment.

## Scripts

Use the `scripts` and `entry_points` features of `setup.py` to automatically create instances of runnable scripts
in the user's environment.

## Example

Consider a new project called "PythonPackaging" that has some command-line scripts, a few packages, and a dependency on a first-party package called [PythonPackagingDependency](https://github.com/DavidAntliff/PythonPackagingDependency).

    /
        bin/               # contains application scripts directly invoked by a user of this package
            do_something.py
            do_something_more.py

        packageA/          # an internal package that contains a module called 'moduleA'
            __init__.py
            moduleA.py

        packageB/          # a second internal package - this one can be 'invoked' (see below)
            __init__.py
            moduleB.py
            __main__.py

        tests/             # contains unit test scripts
            __init__.py
            test_packageA_moduleA.py
            test_packageB_moduleB.py

        README.md
        setup.py           # packaging information file
        requirements.txt   # developer dependencies

[`setup.py`](https://github.com/DavidAntliff/PythonPackaging/blob/master/setup.py) contains rules to provide dependency 
information based on package name and version (`install_requires`) and URLs that can be used to satisfy such dependencies
 (`dependency_links`). See [Dependency Links](https://github.com/DavidAntliff/PythonPackaging#dependency-links) below for more info.

    setup(name="PythonPackaging",
        # ...

        install_requires=[
            "PythonPackagingDependency>=0.0.1",
        ],
        dependency_links=[
            "git+https://github.com/DavidAntliff/PythonPackagingDependency@0.0.1#egg=PythonPackagingDependency-0.0.1",
        ],

        # ...

`setup.py` also contains rules to ensure command-line programs are available after installation:

    setup(name="PythonPackaging",
          # ...

          scripts = ['bin/do_something.py', 'bin/do_something_more.py'],

          entry_points={
              'console_scripts': [
                  'PythonPackaging = packageB.__main__:main',
              ],
          },

          # ...

## Developer Workflow

A virtualenv is recommended.

Assuming developers, not users, wish to hack code on a project, the `pip --editable` option can be used to
install the current working directory as a package in a way that allows code to be edited and immediately
reflected in the installed package.

    pip install --editable --process-dependency-links .

This will install any dependencies into the virtualenv, allowing the scripts and modules to be used in-situ.  

## Installation

Upgrade your `pip`!

    pip install --upgrade pip

### Installation for Users

Users may not be familiar with virtualenv however it is still recommended.

Users install this package into their virtualenv for importing with:

    pip install git+https://@github.com/DavidAntliff/PythonPackaging.git --process-dependency-links

Any dependencies will be fetched by `pip`.

No source directory is created, so the package cannot be edited in this way.

### Installation for Developers

A fresh virtualenv is recommended for each project.

Developers install this package into their virtualenv for editing with:

    pip install --editable git+git@github.com:DavidAntliff/PythonPackaging.git#egg=PythonPackaging --process-dependency-links --src .

Or using HTTPS:

    pip install --editable git+https://github.com/DavidAntliff/PythonPackaging.git#egg=PythonPackaging  --process-dependency-links --src .

Any dependencies will be fetched by `pip`.

This creates a new subdirectory called `pythonpackaging` that contains the source files for this project. Files can be edited here.

Developer dependencies (not required by users) can be manually installed with:

    pip install -r requirements.txt

If required, `requirements.txt` can also specify a URL for a downloadable dependency that will also be editable:

    -e git+git@github.com:DavidAntliff/PythonPackagingDependency@0.0.1#egg=PythonPackagingDependency-0.0.1

## Dependency Links

General requirements:

1. The parent project will specify a required version number for the subordinate project, and
1. The subordinate project must have a `setup.py` that specifies this version number, and
1. The subordinate project's repository must have a tag such that the tagged `setup.py` holds this version number.

In the parent's `setup.py`, the `install_requires` list specifies the package names and versions required by this project.
The `dependency_links` list provides the source URLs for each dependency.
Note the `#egg=PythonPackagingDependency-0.0.1` which is used to tie the URL back to the `install_requires` list.
Note also `@0.0.1` which picks a particular tagged commit from the git repository.
Typically, the tag will match the version number, but this is not strictly necessary.

    install_requires=[
        "PythonPackagingDependency==0.0.1",
    ],
    dependency_links=[
        "git+https://github.com/DavidAntliff/PythonPackagingDependency@0.0.1#egg=PythonPackagingDependency-0.0.1",
    ],

Then when installing the package via `pip`, the option `--process-dependency-links` is required, otherwise the URLs in the `dependency_links` list are ignored:

    pip install git@github.com:Group/Project.git --process-dependency-links

## Limitations

If using [pyenv](https://github.com/pyenv/pyenv), any scripts installed via the `scripts` field in `setup.py` will be placed
into the relevant python version or virtualenv's bin directory, however the shell's PATH will not have this directory included,
so such scripts will not be found in the PATH search. This does not affect the `console_scripts` feature.

