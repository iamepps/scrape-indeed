from selenium import webdriver
import os
# from selenium.webdriver.chrome.options import Options

def initialise_driver():
    options = webdriver.ChromeOptions()

    if os.getenv('ENV')=='local':
        # options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
        options.binary_location = '/usr/bin/google-chrome-stable'
    else:
        options.binary_location = '/usr/bin/google-chrome-stable'
    options.add_argument('headless')
    options.add_argument('no-sandbox')
#    options.add_argument('disable-setuid-sandbox')
    driver = webdriver.Chrome(chrome_options=options)
    return driver
