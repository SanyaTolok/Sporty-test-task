import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options as ChromeOptions
options = ChromeOptions()
options.set_capability('sessionName', 'UI test example')
driver = webdriver.Chrome(options=options)

try:
    # Navigate to twitch page
    driver.get('https://www.twitch.tv/')
    # wait for the page to load and title to contain 'Twitch'
    WebDriverWait(driver, 10).until(EC.title_contains('Twitch'))
    # Click search icon
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
        (By.XPATH, '//*[@id="root"]/div[2]/a[2]/div/div[1]/svg'))).click()
     # wait for the page to load and search bar to exist and enter search term
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
        (By.XPATH, '//input[@type="search"]'))).send_keys('StarCraft II')
    # scroll down two times to load more results
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # wait for the search results to load
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
        (By.XPATH, '//div[@data-a-target="search-result-game"]')))
except NoSuchElementException as err:
    message = 'Exception: ' + str(err.__class__) + str(err.msg)
    # If an element is not found, set the session status to failed
    driver.execute_script(
        'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": ' + json.dumps(message) + '}}')
except Exception as err:
    message = 'Exception: ' + str(err.__class__) + str(err.msg)
    driver.execute_script(
        'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": ' + json.dumps(message) + '}}')
finally:
    # Stop the driver
    driver.quit()
