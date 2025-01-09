import smtplib
import ssl
from email.mime.text import MIMEText
from typing import Final

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
            print(f'Error: {e}')
