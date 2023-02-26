import smtplib
import ssl
from app_data import SENDER, PASSWORD, RECEIVER


def send_email(message):
    host = "smtp.gmail.com"
    port = 465

    username = SENDER
    password = PASSWORD

    receiver = RECEIVER
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver, message)
    print("Email was sent!")


if __name__ == "__main__":
    print(SENDER)
    print(PASSWORD)
    print(RECEIVER)
