import logging.config
from os import path

log_file_path = path.join(path.dirname(path.abspath(__file__)), "logging.ini")
logging.config.fileConfig(log_file_path)


pytest_plugins = [
    "final.src.fixtures",
    "final.src.actions.base",
]


def pytest_addoption(parser):
    parser.addini("selenium_url", "Selenium hub url")
    parser.addini("browser_name", "Browser name")
