from twilio.rest import Client
import requests
import logging

logging.basicConfig(filename='app.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')


class Message:
    def __init__(self, account_sid, auth_token, twilio_phone_number, my_phone_number) -> None:
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.twilio_phone_number = twilio_phone_number
        self.my_phone_number = my_phone_number

    def send_sms(self, message='Testing 1, Testing 2') -> str:
        client = Client(self.account_sid, self.auth_token)
        message = client.messages.create(
            body=message,
            from_=self.twilio_phone_number,
            to=self.my_phone_number
        )
        return message.sid

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
