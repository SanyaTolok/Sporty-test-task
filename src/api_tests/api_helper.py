import requests
import json

class APIHelper:
    def __init__(self, base_url: str = ""):
        self.base_url = base_url

    def _send_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        url = f"{self.base_url}{endpoint}" if self.base_url and not endpoint.startswith(('http://', 'https://')) else endpoint
        
        print(f"Making {method} request to: {url}")
        print(f"Request parameters: {kwargs}")

        try:
            response = requests.request(method, url, **kwargs)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
            print(f"Response status code: {response.status_code}")
            return response
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error for {method} {url}: {e}")
            print(f"Response text: {e.response.text}")
            raise
        except requests.exceptions.ConnectionError as e:
            print(f"Connection Error for {method} {url}: {e}")
            raise
        except requests.exceptions.Timeout as e:
            print(f"Timeout Error for {method} {url}: {e}")
            raise
        except requests.exceptions.RequestException as e:
            print(f"An unexpected error occurred for {method} {url}: {e}")
            raise

    def get(self, endpoint: str, params: dict = None, headers: dict = None) -> requests.Response:
        return self._send_request('GET', endpoint, params=params, headers=headers)

    def post(self, endpoint: str, data: dict = None, json_data: dict = None, headers: dict = None) -> requests.Response:
        return self._send_request('POST', endpoint, data=data, json=json_data, headers=headers)

    def put(self, endpoint: str, data: dict = None, json_data: dict = None, headers: dict = None) -> requests.Response:
        return self._send_request('PUT', endpoint, data=data, json=json_data, headers=headers)

    def delete(self, endpoint: str, params: dict = None, headers: dict = None, **kwargs) -> requests.Response:
        return self._send_request('DELETE', endpoint, params=params, headers=headers, **kwargs)
    def patch(self, endpoint: str, data: dict = None, json_data: dict = None, headers: dict = None) -> requests.Response:
        return self._send_request('PATCH', endpoint, data=data, json=json_data, headers=headers)