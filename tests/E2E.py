
from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from time import sleep
from selenium.webdriver.common.by import By

test_url = 'https://www.youtube.com/shorts/N-etpkOVBMM'
core_url = 'https://summ3ry.r2d2.pl/'
summary_url = core_url + 'summary'

def endToEndUrl():
    TIMEOUT = 300
    """
    params:
    TIMEOUT: INT

    Description:
    Test verifies whether a summary is response within specified timeout upon url submission
    """
    driver = webdriver.Firefox()
    driver.get('https://summ3ry.r2d2.pl/')
    url_from = driver.find_element(By.ID, "url")
    submit_url_btn = driver.find_element(By.ID, "url-button")

    # paste and submit url
    url_from.send_keys(test_url)
    submit_url_btn.click()
    # wait until summary page loads
    try:
        summary = WebDriverWait(driver, TIMEOUT).until(expected_conditions.url_changes(summary_url))
    except TimeoutError: 
        print('timeout failed on url submit')

    # test transcript downloads
    # TODO

    driver.close()