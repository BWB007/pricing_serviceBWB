import os
from typing import List
from requests import Response, post

__author__ = 'benbrown'


class MailgunException(Exception):
    def __init__(self, message: str):
        self.message = message


class Mailgun():

    FROM_TITLE = 'Pricing Service'
    @classmethod
    def send_mail(cls, email: List[str], subject: str, text: str, html: str) -> Response:
        api_key = os.environ.get('MAILGUN_API_KEY', None)
        domain = os.environ.get('MAILGUN_DOMAIN', None)
        from_email = os.environ.get('MAILGUN_FROM', None)

        if api_key is None:
            raise MailgunException('Failed to load Mailgun API key.')

        if domain is None:
            raise MailgunException('Failed to load Mailgun domain.')

        if from_email is None:
            raise MailgunException('Failed to load Mailgun from emai.')
        response = post(f"{domain}/messages",
            auth=("api", api_key),
            data={"from": f"{cls.FROM_TITLE} <{from_email}>",
                  "to": email,
                  "subject": subject,
                  "text": text,
                  "html": html})
        if response.status_code != 200:
            print(response.json())
            raise MailgunException('An error occurred while sending email.')
        return response

