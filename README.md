## Example of simple API tests for yandex disk [(swagger)](https://tech.yandex.ru/disk/poligon/#!/v1/)
Used packages: Requests + Pytest + Allure2

## Requirements:
1. Python 3.6
2. [Allure2 report generator](https://github.com/allure-framework/allure2#download) (add allure to PATH variables)

## Setup and Run:
(Terminal from root project folder)
1. Install Python dependencies: `. ./scripts/install_deps.sh`
2. Get token for yandex disk [here](https://tech.yandex.ru/disk/poligon/#!//v1/)
3. Set it in environment variable: `export TOKEN='your_token'`
4. Run tests and get report: `. ./scripts/run_tests_and_make_report.sh`

## Main idea:
1. One folder will be created in your disk
2. All test data will be created inside it
3. After test run folder with all test data will be deleted to trash folder
