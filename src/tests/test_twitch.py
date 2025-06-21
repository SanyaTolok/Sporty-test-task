import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


@pytest.fixture(scope="module")
def browser():
    mobile_emulation = {
        "deviceMetrics": { "width": 375, "height": 812, "pixelRatio": 3 }, # iPhone X dimensions
        "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Mobile/15E148 Safari/604.1"
    }
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    driver = webdriver.Chrome(options=chrome_options)

    driver.maximize_window() 
    yield driver 
    driver.quit() 

def test_open_twitch_web_app(browser):
    twitch_url = "https://www.twitch.tv/"
    expected_title_part = "Twitch"
    expected_url_start = "https://m.twitch.tv/?desktop-redirect=true"

    print(f"\nAttempting to open Twitch at: {twitch_url}")
    browser.get(twitch_url) # Navigate to the Twitch URL

    # Wait for the page title to contain "Twitch" for up to 10 seconds.
    # This helps ensure the page has loaded before proceeding.
    try:
        WebDriverWait(browser, 5).until(
            EC.title_contains(expected_title_part)
        )
        print(f"Page title found containing '{expected_title_part}': {browser.title}")
    except Exception as e:
        pytest.fail(f"Twitch page title not found or page did not load: {e}")
    current_url = browser.current_url
    assert current_url.startswith(expected_url_start), \
        f"Expected URL to start with '{expected_url_start}', but got '{current_url}'"
        # Wait for the main content to be visible
    print("Twitch page loaded successfully and main content is visible.")
    try:
        # accept coocies
        browser.find_element(By.XPATH, '//button[@data-a-target="consent-banner-accept"]').click()
        # Click search icon
        WebDriverWait(browser, 5).until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="root"]/div[2]/a[2]'))).click()
        # wait for the page to load and search bar to exist and click on it
        WebDriverWait(browser, 5).until(EC.visibility_of_element_located(
            (By.XPATH, '//input[@type="search"]')))
        # Enter search term 'StarCraft II'
        WebDriverWait(browser, 5).until(EC.visibility_of_element_located(
            (By.XPATH, '//input[@type="search"]'))).send_keys('StarCraft II')
        browser.implicitly_wait(5) 
        browser.find_element(By.XPATH, '//img[@alt="StarCraft II"]').click()
        print("scroll down two times to load more results")
        actions = ActionChains(browser)
        # Alternative way to scroll down using ActionChains
        # actions.send_keys(Keys.PAGE_DOWN).perform()
        # import time
        # time.sleep(3) 
        # actions.send_keys(Keys.PAGE_DOWN).perform()
        # time.sleep(3) 
        browser.execute_script("window.scrollBy(0, window.innerHeight);")
        import time
        time.sleep(1) 
        browser.execute_script("window.scrollBy(0, window.innerHeight);")
        time.sleep(1) 
        print("Click on visible streamer in the search results ")
        WebDriverWait(browser, 5).until(EC.visibility_of_element_located(
            (By.XPATH, '//a[contains(@class, "tw-link")]')))
        actions.move_to_element(
            browser.find_element(By.XPATH, '//a[contains(@class, "tw-link")]')).click().perform()
        # Wait for the streamer page to load (Note I didn't found any of streamers with discleamer on a page that is why this step is missed but it can be handled with simpe if else statement
        WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//div[@data-a-target="player-overlay-click-handler"]'))
        )
        WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//button[@aria-label="Follow "]'))
        )
        WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//section[@id="channel-player-disclosures"]'))
        )
        WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//button[@data-a-target="chat-settings"]'))
        )
        WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//button[@aria-label="More channel actions"]'))
        )
        WebDriverWait(browser, 5).until(
            EC.visibility_of_element_located((By.XPATH, '//div[@data-a-target="video-ref"]'))
        )
        WebDriverWait(browser, 5).until(
            EC.visibility_of_element_located((By.XPATH, '//div[@aria-label="Send a message"]'))
        )
        WebDriverWait(browser, 5).until(
            EC.invisibility_of_element((By.XPATH, '//div[contains(text(), "Connecting to Chat")]'))
        )
        print("Streamer page loaded successfully.")
        browser.save_screenshot("twitch_streamer_page.png")
    finally:
        if browser:
            print("Closing the browser...")
            browser.quit()
        else:
            print("Driver was not initialized, nothing to close.")
