import os
from selenium import webdriver
from sys import platform


def initialise_driver():
    options = webdriver.ChromeOptions()

    if platform == "linux" or platform == "linux2":
        options.binary_location = '/usr/bin/google-chrome'
        # options.binary_location = '/usr/bin/google-chrome-stable'
    elif platform == "darwin":
        options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'

    options.add_argument('headless')
    options.add_argument('no-sandbox')

    driver = webdriver.Chrome(chrome_options=options)
    return driver
