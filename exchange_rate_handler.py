import requests
from requests.structures import CaseInsensitiveDict
import pprint
import logging

logging.basicConfig(filename='app.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')


class Exchange_rate:
    def __init__(self, api_key) -> None:
        self.api_key = api_key

    def get_exchange_rates(self):
        url = 'https://api.freecurrencyapi.com/v1/latest'
        headers = CaseInsensitiveDict()
        headers['apikey'] = self.api_key
        response = requests.get(url, headers=headers)
        data = response.json()

        # Print the entire response JSON for debugging
        # pprint.pprint(data)

        # Check the correct structure and access keys accordingly
        if 'data' in data:
            rates = data['data']
            return rates['JPY'], rates['AUD']
        else:
            raise KeyError(
                "The key 'data' was not found in the response JSON.")

    def check_network(self) -> bool:
        url: str = 'https://www.google.com'
        retries: int = 3
        timeout: int = 10
        for attempt in range(retries):
            try:
                response = requests.get(url, timeout=timeout)
                if response.status_code == 200:
                    return True
            except requests.ConnectionError as e:
                logging.error(f"Network check attempt {
                              attempt + 1} failed: {e}")
            except requests.Timeout as e:
                logging.error(f"Network check attempt {
                              attempt + 1} timed out: {e}")
        return False
