"""
Server Status Checker

A server status checker is a script that will let you monitor if your server is active and running.
It can show you how much downtime your server has had and give you regular updates.
It'll also send immediate alerts through gmail when server is down.
"""
import socket
import time
from datetime import datetime, timedelta, timezone
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate


IP = "google.com"  # Enter IP or domain
PORT = 80


country_time = timezone(timedelta(hours=9), "JST")  # Set your timezone.


def send_email(time_down):
    """
    The function sends an email to the destination address when the server is down.
    It writes

    """

    # Gmail Login Information
    send_address = "your adress"
    password = (
        "yourpassword"  # You may need to create "app password" through Google.
    )

    # SMTP Connection
    server = smtplib.SMTP("smtp.gmail.com", 587)  # Gmail SMTP server
    server.starttls()
    server.login(send_address, password)

    # Mail Message
    subject = f"Attention, {IP} is down"
    from_address = "Server Status Checker"  # This is the sender's email name.
    to_address = "example@example.com"  # The destination email address.
    body_text = f"{time_down} {IP} is down"
    # --------------------- #
    msg = MIMEText(body_text)
    msg["Subject"] = subject
    msg["From"] = from_address
    msg["To"] = to_address
    msg["Date"] = formatdate()

    # Sending the email
    server.send_message(msg)
    server.close()


def main():
    """
    It checks if the server is up or down, and if it's down, it sends an email
    """

    time.sleep(15)  # Wait 15 seconds before checking again.
    time_now = datetime.now(country_time).strftime("%Y-%m-%d %H:%M:%S")
    try:
        socket.create_connection((IP, PORT), 2)
        print(f"\x1b[32m {time_now}  {IP} is up \x1b[0m")
        with open("log.txt", "a", encoding="utf8") as log:
            log.write(f"{time_now} {IP} is up\n")
    except OSError:
        print(f"\x1b[31m {time_now}  {IP} is down\x1b[0m")
        # Send email
        send_email(time_now)
        with open("log.txt", "a", encoding="utf8") as log:
            log.write(f"\n{time_now} {IP} is down\n")


try:
    # Starting checker
    print("\n\t--- Starting checker ---\n")
    while 1:
        main()


except KeyboardInterrupt:
    print("\n\t--- Exiting checker ---\n")
    exit()
