#!/usr/bin/env bash

rm -rf allure-results

# there is an issue https://github.com/pypa/pipenv/issues/2092
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8

pipenv run python -m pytest tests -l -v -vv -s

allure serve allure-results
