# Sporty-test-task
This repostory contains test task for sporty. In project used Python/Selenium//PIP for UI tests and Python/Request/Pytest/PIP for API tests.

## Instalation
install the required packages
pip3 install -r /Sporty-test-task/src/requirements.txt

## UI Tests 
Tests are located in /Sporty-test-task/src/tests/

### Run tests using mobile emulator
cd src (in case if you are not in src derectory)

pytest --env mobile -s -v

### Run tests using desctop resolution
pytest --env desktop -s -v
Note env was added in oder to have ability to extend tests and has ability to scale test but tests itself are designed for mobile view


https://github.com/user-attachments/assets/71573681-2dd5-4d13-9731-b1d58b45129b


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

### Run API tests
To run tests use: pytest -v -s flights_tests.py --html=report.html --self-contained-html
Report example see report.html
<img width="2237" alt="Screenshot 2025-06-21 at 00 07 31" src="https://github.com/user-attachments/assets/d465047b-f406-4b26-b63a-041409a86f60" />
