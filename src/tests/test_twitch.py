import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from browser_helper import driver  


def test_for_twitch_streamer_page_from_search(driver):
    twitch_url = "https://www.twitch.tv/"
    expected_title_part = "Twitch"
    expected_url_start = "https://m.twitch.tv/?desktop-redirect=true"

    print(f"\nAttempting to open Twitch at: {twitch_url}")
    driver.get(twitch_url) # Navigate to the Twitch URL

    # Wait for the page title to contain "Twitch" for up to 10 seconds.
    # This helps ensure the page has loaded before proceeding.
    try:
        WebDriverWait(driver, 5).until(
            EC.title_contains(expected_title_part)
        )
        print(f"Page title found containing '{expected_title_part}': {driver.title}")
    except Exception as e:
        pytest.fail(f"Twitch page title not found or page did not load: {e}")
    current_url = driver.current_url
    assert current_url.startswith(expected_url_start), \
        f"Expected URL to start with '{expected_url_start}', but got '{current_url}'"
        # Wait for the main content to be visible
    print("Twitch page loaded successfully and main content is visible.")
    try:
        # accept coocies
        driver.find_element(By.XPATH, '//button[@data-a-target="consent-banner-accept"]').click()
        # Click search icon
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="root"]/div[2]/a[2]'))).click()
        # wait for the page to load and search bar to exist and click on it
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located(
            (By.XPATH, '//input[@type="search"]')))
        # Enter search term 'StarCraft II'
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located(
            (By.XPATH, '//input[@type="search"]'))).send_keys('StarCraft II')
        driver.implicitly_wait(5) 
        driver.find_element(By.XPATH, '//img[@alt="StarCraft II"]').click()
        print("scroll down two times to load more results")
        actions = ActionChains(driver)
        # Alternative way to scroll down using ActionChains
        # actions.send_keys(Keys.PAGE_DOWN).perform()
        # import time
        # time.sleep(3) 
        # actions.send_keys(Keys.PAGE_DOWN).perform()
        # time.sleep(3) 
        driver.execute_script("window.scrollBy(0, window.innerHeight);")
        import time
        time.sleep(1) 
        driver.execute_script("window.scrollBy(0, window.innerHeight);")
        time.sleep(1) 
        print("Click on visible streamer in the search results ")
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located(
            (By.XPATH, '//a[contains(@class, "tw-link")]')))
        actions.move_to_element(
            driver.find_element(By.XPATH, '//a[contains(@class, "tw-link")]')).click().perform()
        # Wait for the streamer page to load (Note I didn't found any of streamers with discleamer on a page that is why this step is missed but it can be handled with simpe if else statement
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//div[@data-a-target="player-overlay-click-handler"]'))
        )
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//button[@aria-label="Follow "]'))
        )
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//section[@id="channel-player-disclosures"]'))
        )
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//button[@data-a-target="chat-settings"]'))
        )
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//button[@aria-label="More channel actions"]'))
        )
        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, '//div[@data-a-target="video-ref"]'))
        )
        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, '//div[@aria-label="Send a message"]'))
        )
        WebDriverWait(driver, 5).until(
            EC.invisibility_of_element((By.XPATH, '//div[contains(text(), "Connecting to Chat")]'))
        )
        print("Streamer page loaded successfully.")
        driver.save_screenshot("twitch_streamer_page.png")
    finally:
        if driver:
            print("Closing the browser...")
            driver.quit()
        else:
            print("Driver was not initialized, nothing to close.")
