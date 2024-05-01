import os
import ssl
import smtplib

from email.mime.text import MIMEText

from typing import Final

EMAIL_API: Final = os.getenv("EMAIL_API")
EMAIL_API_KEY: Final = os.getenv("EMAIL_API_KEY")

TARGET_EMAIL_SENDER: Final = os.getenv("TARGET_EMAIL_SENDER")


def send_email(
    subject: str,
    body: str,
) -> None:
    message = MIMEText(body)

    message["Subject"] = subject
    message["From"] = EMAIL_API
    message["To"] = TARGET_EMAIL_SENDER

    text = message.as_string()

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(EMAIL_API, EMAIL_API_KEY)
        server.sendmail(EMAIL_API, TARGET_EMAIL_SENDER, text)
