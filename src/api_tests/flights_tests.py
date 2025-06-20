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

def test_get_flights_success(aviationstack_helper, api_key):
    """
    Test case to verify a successful GET request to the /flights endpoint.
    Checks for a 200 OK status code and that the response contains data.
    """
    try:
        params = {"access_key": api_key, "limit": 5}
        response = aviationstack_helper.get("flights", params=params)
        assert response.status_code == 200
        response_json = response.json()
        assert "data" in response_json
        assert isinstance(response_json["data"], list)
        assert len(response_json["data"]) > 0, "Expected flight data, but none was returned."
        print("Successfully retrieved flight data.")
        print(f"Sample flight data (first entry): {json.dumps(response_json['data'][0], indent=2)}")

    except requests.exceptions.RequestException as e:
        pytest.fail(f"Test failed due to RequestException: {e}")

def test_get_flights_with_status_param(aviationstack_helper, api_key):
    """
    Test case to verify GET request to /flights with a 'flight_status' parameter.
    Checks for 200 OK and that results generally match the requested status.
    """
    print("\n--- Running test_get_flights_with_status_param ---")
    try:
        flight_status = "landed" # Example: test for 'landed' flights
        params = {"access_key": api_key, "flight_status": flight_status, "limit": 5}
        response = aviationstack_helper.get("flights", params=params)

        assert response.status_code == 200
        response_json = response.json()
        assert "data" in response_json
        assert isinstance(response_json["data"], list)

        # Verify that returned flights generally match the 'landed' status
        # Note: API might return empty list if no flights match criteria at the moment
        if response_json["data"]:
            print(f"Sample flight data with status '{flight_status}' (first entry): {json.dumps(response_json['data'][0], indent=2)}")
            # This is a soft check, as the 'flight_status' in response might be in a nested structure
            # A more robust test would iterate and check each flight object
            assert any(flight.get('flight_status') == flight_status for flight in response_json["data"]) or \
                   any(flight.get('flight', {}).get('status') == flight_status for flight in response_json["data"]), \
                   f"No flights with status '{flight_status}' found or status field missing."
        else:
            print(f"No flights found for status: {flight_status}")

    except requests.exceptions.RequestException as e:
        pytest.fail(f"Test failed due to RequestException: {e}")

def test_get_flights_invalid_api_key(aviationstack_helper):
    """
    Test case to verify handling of an invalid API key.
    Expects a 401 Unauthorized status code.
    """
    print("\n--- Running test_get_flights_invalid_api_key ---")
    try:
        params = {"access_key": "INVALID_API_KEY"}
        with pytest.raises(requests.exceptions.HTTPError) as excinfo:
            aviationstack_helper.get("flights", params=params)
        
        assert excinfo.value.response.status_code == 401
        print("Successfully caught 401 Unauthorized for invalid API key.")

    except requests.exceptions.RequestException as e:
        pytest.fail(f"Test failed due to an unexpected RequestException: {e}")

def test_get_flights_missing_api_key(aviationstack_helper):
    """
    Test case to verify handling of a missing API key.
    Expects a 401 Unauthorized status code.
    """
    print("\n--- Running test_get_flights_missing_api_key ---")
    try:
        # No access_key param provided
        with pytest.raises(requests.exceptions.HTTPError) as excinfo:
            aviationstack_helper.get("flights") 
        
        assert excinfo.value.response.status_code == 401
        print("Successfully caught 401 Unauthorized for missing API key.")

    except requests.exceptions.RequestException as e:
        pytest.fail(f"Test failed due to an unexpected RequestException: {e}")
