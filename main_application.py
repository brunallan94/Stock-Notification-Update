from exchange_rate_handler import Exchange_rate
from message_handler import Message
from dotenv import load_dotenv
from tqdm import tqdm
import os
import logging
import time

logging.basicConfig(filename='app.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def configure() -> None:
    load_dotenv()


def main() -> None:
    configure()

    steps: list[str] = ['Checking network for exchange rates',
                        'Fetching exchange rates', 'Checking network for SMS', 'Sending SMS']
    progress_bar = tqdm(total=len(steps), desc='Progress',
                        bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} {desc}')

    exchange_rate_handler = Exchange_rate(os.getenv('exchange_rates_api_key'))
    message_handler = Message(
        os.getenv('twilio_account_sid'), os.getenv('twilio_auth_token'), os.getenv('twilio_phone_number'), os.getenv('my_phone_number'))

    progress_bar.set_description(steps[0])

    if not exchange_rate_handler.check_network():
        logging.warning(
            'Network is not available. Please check your connection and try again')
        return
    progress_bar.update(1)

    try:
        progress_bar.set_description(steps[1])
        usd_to_jpy, usd_to_aud = exchange_rate_handler.get_exchange_rates()
        message = f"Exchange Rates: \n1 USD = {
            usd_to_jpy} JPY\n1 USD = {usd_to_aud} AUD"
        progress_bar.update(1)

        progress_bar.set_description(steps[2])
        if not message_handler.check_network():
            logging.warning(
                'Network is not available for sending SMS. Please check your connection and try again.')
            return
        progress_bar.update(1)

        progress_bar.set_description(steps[3])
        sms_sid = message_handler.send_sms(message)
        logging.info(f'SMS sent successfully with SID: {sms_sid}')
        progress_bar.update(1)

    except KeyError as e:
        logging.error(f'Failed to get exchange rates: {e}')
    except Exception as e:
        logging.error(f'An error occurred: {e}')

    progress_bar.close()
