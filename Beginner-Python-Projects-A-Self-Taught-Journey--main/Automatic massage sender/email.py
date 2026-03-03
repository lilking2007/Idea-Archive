#pip install smtplib

import smtplib
import schedule
import time

def send_email():
    sender_email = "ryanmaiyo52@gmail.com"
    receiver_email = "kipchumbaryan2007@gmail.com"
    password = "Ryan.kipchumba@2007"
    
    subject = "Automated Email"
    body = "Hello! This is an automated email."

    message = f"Subject: {subject}\n\n{body}"

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

    print("Email sent!")

schedule.every().day.at("08:00").do(send_email)

while True:
    schedule.run_pending()
    time.sleep(1)
