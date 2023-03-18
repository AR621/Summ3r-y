
from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from time import sleep
from selenium.webdriver.common.by import By


test_url = 'https://www.youtube.com/shorts/N-etpkOVBMM'
core_url = 'http://localhost:5000'
summary_url = '/summary'


def test_end_to_end_url():
    TIMEOUT = 300
    """
    params:
    TIMEOUT: INT

    Description:
    Test verifies whether a summary is response within specified timeout upon url submission
    """
    # add headless options for CI
    opt = webdriver.FirefoxOptions()
    opt.add_argument('--headless')

    driver = webdriver.Firefox(options=opt)
    driver.get(core_url)
    url_from = driver.find_element(By.ID, "url")
    submit_url_btn = driver.find_element(By.ID, "url-button")

    # paste and submit url
    url_from.send_keys(test_url)
    submit_url_btn.click()
    # wait until summary page loads
    summary = WebDriverWait(driver, TIMEOUT).until(expected_conditions.url_contains(summary_url))
        
    # test transcript downloads
    # TODO

    driver.close()