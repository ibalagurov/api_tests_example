#!/usr/bin/env bash
rm -rf allure-results

python3 -m pytest tests -l -v -vv -s

allure serve allure-results
