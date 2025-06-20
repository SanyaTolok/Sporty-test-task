import pytest
import os
import json

import requests
from api_helper import APIHelper 

@pytest.fixture(scope="module")
def api_key():
    key = os.getenv("AVIATIONSTACK_API_KEY")
    if not key:
        pytest.fail("AVIATIONSTACK_API_KEY environment variable is not set. "
                     "Please set it before running tests.")
    return key

@pytest.fixture(scope="module")
def aviationstack_helper(api_key):
    return APIHelper(base_url="https://api.aviationstack.com/v1/")

def test_get_routes_success(aviationstack_helper, api_key):
    """
    Test case to verify a successful GET request to the /routes endpoint.
    Checks for a 200 OK status code and that the response contains data.
    """
    print("\n--- Running test_get_routes_success ---")
    try:
        params = {"access_key": api_key, "limit": 5} # Limit to 5 for quicker response
        response = aviationstack_helper.get("routes", params=params)

        assert response.status_code == 200
        response_json = response.json()
        assert "data" in response_json
        assert isinstance(response_json["data"], list)
        assert len(response_json["data"]) > 0, "Expected route data, but none was returned."
        print("Successfully retrieved route data.")
        print(f"Sample route data (first entry): {json.dumps(response_json['data'][0], indent=2)}")

    except requests.exceptions.RequestException as e:
        pytest.fail(f"Test failed due to RequestException: {e}")
