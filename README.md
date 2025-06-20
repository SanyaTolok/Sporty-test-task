# Sporty-test-task
This repostory contains test task for sporty. In project used Python/Selenium/Browserstack/PIP. Core of framework uses https://www.browserstack.com/docs/automate/selenium/getting-started/python.
## Instalation
### create virtual environment
python3 -m venv env
source env/bin/activate
### install the required packages
pip3 install -r /Sporty-test-task/src/requirements.txt
## Tests 
Tests are located in /Sporty-test-task/src/tests/
### Run tests
    cd src
    browserstack-sdk pytest -s ~/Sporty-test-task/src/tests/
## API tests
API tests are done using pytest and python request library
For testing used Aviationstack API which is list in https://github.com/public-apis/public-apis
Covered test cases:
Verify ability to get flights list without API key
Verify ability to get flights list with API key
Verify ability to get flights history
Verify ability to get flights rotes 

