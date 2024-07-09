import requests
from requests.structures import CaseInsensitiveDict
import pprint


def get_exchange_rates():
    url = 'https://api.freecurrencyapi.com/v1/latest'
    headers = CaseInsensitiveDict()
    headers['apikey'] = 'fca_live_HSQGUYqDFIA8sihuzS8Chn15CU7Wm8pUdOO8mA0n'
    response = requests.get(url, headers=headers)
    data = response.json()

    # Print the entire response JSON for debugging
    pprint.pprint(data)

    rate = data['data']['JPY']
    pprint.pprint(f'1 USD = {rate} Japanese Yen')


get_exchange_rates()
