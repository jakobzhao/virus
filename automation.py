import smtplib
import ssl

port = 465  # For SSL
smtp_server = "smtp.gmail.com"
receiver_email = open("steven_gmail_password", "r").read().split("\n")[0]
sender_email = open("steven_gmail_password", "r").read().split("\n")[1]
password = open("steven_gmail_password", "r").read().split("\n")[2]
message = """\
Subject: Data Update Error - COVID-19 Website 

There are errors while updating the database. Please check."""

context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)