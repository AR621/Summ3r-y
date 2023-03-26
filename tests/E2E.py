import os
from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from time import sleep
from selenium.webdriver.common.by import By


TEST_URL = 'https://www.youtube.com/shorts/N-etpkOVBMM'
CORE_URL = 'http://localhost:5000'
SUMMARY_URL = '/summary'
ABS = os.path.abspath(os.path.join(os.getcwd(), 'tests'))
TEST_FILE = os.path.join(ABS,'sample.mp3')


def test_E2E_url():
    TIMEOUT = 300
    """
    params:
    TIMEOUT: INT
    Description:
    Test verifies whether a summary is response within specified timeout upon url submission
    """
    # add headless options for CI
    opt = webdriver.ChromeOptions()
    # opt.add_argument('--headless')
    driver = webdriver.Chrome(options=opt)
    driver.get(CORE_URL)
    
    url_from = driver.find_element(By.ID, "url")
    submit_url_btn = driver.find_element(By.ID, "url-button")

    # paste and submit url
    url_from.send_keys(TEST_URL)
    submit_url_btn.click()
    # wait until summary page loads
    summary = WebDriverWait(driver, TIMEOUT).until(expected_conditions.url_changes(SUMMARY_URL))
    
    # test transcript downloads
    transcript_download = driver.find_element(By.ID, "transcript")
    assert transcript_download.get_attribute('href')

    summary_download = driver.find_element(By.ID, "summary")
    assert summary_download.get_attribute('href')
    
    driver.close()
    
    
def test_E2E_file():
    TIMEOUT = 300
    """
    params:
    TIMEOUT: INT
    Description:
    Test verifies whether a summary is response within specified timeout upon file submission
    """
    # add headless options for CI
    opt = webdriver.ChromeOptions()
    # opt.add_argument('--headless')
    driver = webdriver.Chrome(options=opt)
    driver.get(CORE_URL)
    
    file_from = driver.find_element(By.ID, "formFile")
    submit_file_btn = driver.find_element(By.ID, "audio-file-button")

    # paste and submit url
    file_from.send_keys(TEST_FILE)
    submit_file_btn.click()
    # wait until summary page loads
    summary = WebDriverWait(driver, TIMEOUT).until(expected_conditions.url_changes(SUMMARY_URL))
    
    # test transcript downloads
    transcript_download = driver.find_element(By.ID, "transcript")
    assert transcript_download.get_attribute('href')

    summary_download = driver.find_element(By.ID, "summary")
    assert summary_download.get_attribute('href')

    driver.close()