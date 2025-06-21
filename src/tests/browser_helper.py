import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(scope="function")
def driver(request):
    env = request.config.getoption("--env")
    current_driver = None

    if env == "mobile":
        chrome_options = Options()
        # Configure Chrome for mobile emulation
        mobile_emulator = {
            "deviceMetrics": { "width": 375, "height": 812, "pixelRatio": 3 }, # iPhone X dimensions
            "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Mobile/15E148 Safari/604.1"
        }
        chrome_options.add_experimental_option("mobileEmulation", mobile_emulator)
        current_driver = webdriver.Chrome(options=chrome_options)
        print("Mobile Web Driver initialized.")

    elif env == "desktop":
        # Standard desktop browser setup
        chrome_options = Options()
        # You can add other desktop specific options here if needed
        # e.g., chrome_options.add_argument("--incognito")
        current_driver = webdriver.Chrome(options=chrome_options)
        current_driver.maximize_window() # Maximize for desktop view
        print("Desktop Web Driver initialized.")

    else:
        # Fallback or error for unknown environments
        raise ValueError(f"Unknown environment specified: {env}. Use 'mobile' or 'desktop'.")

    # Yield the driver to the test function
    yield current_driver

    # Teardown: Quit the driver after the test is done
    if current_driver:
        current_driver.quit()
        print(f"Driver for {env} environment quit.")