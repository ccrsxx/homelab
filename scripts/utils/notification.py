import smtplib
import ssl
from email.mime.text import MIMEText
from typing import Final

import requests

from .env import app_env


def send_email(
    subject: str,
    body: str,
) -> None:
    message = MIMEText(body)

    message['Subject'] = subject
    message['From'] = app_env.EMAIL_API
    message['To'] = app_env.TARGET_EMAIL_SENDER

    text = message.as_string()

    context = ssl.create_default_context()

    MAX_EMAIL_ATTEMPTS: Final = 3

    for _ in range(MAX_EMAIL_ATTEMPTS):
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
                server.login(app_env.EMAIL_API, app_env.EMAIL_API_KEY)
                server.sendmail(app_env.EMAIL_API, app_env.TARGET_EMAIL_SENDER, text)
                break
        except Exception as e:
            print(f'Failed to send email: {e}')


def send_pushover(
    message: str,
) -> bool:
    url = 'https://api.pushover.net/1/messages.json'

    payload = {
        'user': app_env.PUSHOVER_USER,
        'token': app_env.PUSHOVER_TOKEN,
        'message': message,
    }

    try:
        response = requests.post(url, data=payload, timeout=10)
        response.raise_for_status()
        return True
    except requests.RequestException as e:
        print(f'Failed to send Pushover message: {e}')
        return False


def send_discord(
    message: str,
) -> bool:
    url = f'https://discord.com/api/webhooks/{app_env.DISCORD_WEBHOOK_ID}/{app_env.DISCORD_WEBHOOK_TOKEN}'

    payload = {
        'content': message,
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        return True
    except requests.RequestException as e:
        print(f'Failed to send Discord message: {e}')
        return False
