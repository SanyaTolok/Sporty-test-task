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
1.  Test case to verify a successful GET request to the /flights endpoint.
    Checks for a 200 OK status code and that the response contains data.
2.  Test case to verify GET request to /flights with a 'flight_status' parameter.
    Checks for 200 OK and that results generally match the requested status.
3. Test case to verify handling of an invalid API key.
    Expects a 401 Unauthorized status code.
4.  Test case to verify handling of a missing API key.
    Expects a 401 Unauthorized status code.

## Run tests
To run tests use: pytest -v -s flights_tests.py --html=report.html --self-contained-html
Report example see report.html

<img width="2240" alt="Screenshot 2025-06-21 at 00 06 21" src="https://github.com/user-attachments/assets/45f505ae-ce03-4e58-9400-8278941d89c1" />


