# flying-brick
[![Build Status](https://travis-ci.com/stfab/flying-brick.svg?branch=master)](https://travis-ci.com/stfab/flying-brick)
[![Version](https://img.shields.io/github/pipenv/locked/python-version/stfab/flying-brick)](https://github.com/stfab/flying-brick)
[![License](https://img.shields.io/github/license/stfab/flying-brick)](https://github.com/stfab/flying-brick)
[![OS](https://img.shields.io/badge/os-win%20x64%20%7C%20linux%20x64-lightgrey)](https://github.com/stfab/flying-brick)


A simple game where you navigate a jumping brick through hindrances.

![test](https://github.com/stfab/flying-brick/raw/master/preview.jpg)

## Usage

### Build

* Install Python 3.7.
* Install the package manager pip3.
* Install pipenv and tox with `pip3 install pipenv`.
* Install the necessary packages with `pipenv install`.

### Execute

Start the game with `pipenv run python src/main.py`.

### Simulate

Simulate the game with `pipenv run python src/main.py --simulate`

## Develop and Contribute

* Open an issue to get it accepted or begin working on an existing and accepted issue.
* Make sure you fork the repository into your own repository.
* Afterwards clone the repository locally on your machine.

### Build

* Install Python 3.7.
* Install the package manager pip3.
* Install pipenv and tox with `pip3 install pipenv`.
* Install the necessary packages and dev packages with `pipenv install --dev`.

### Test

Run the tests locally in an isolated environment via `pipenv run tox`.

If it works correctly you can start implementing your changes.

### Build the Docs

If you want to contribute to the docs try to build them first via `pipenv run tox -e build-docs`.

If this works as well you can continue.

### Travis CI

flying-brick is tested via Travis CI on different architectures.

To set up Travis CI so that it tests each commit, make a new account and give Travis CI permission
to your fork.

Now every new commit triggers a build and test run that is described in .travis.yml.

### Precommit

Commit your changes locally.

For every change add tests under src/tests.py if possible.

Make sure all tests work with tox (additionally check if the docs are built correctly).

Push your changes to your fork and let Travis CI run correctly.

### Commit

Open a pull request to the main repository and link it with the issue you solved.

