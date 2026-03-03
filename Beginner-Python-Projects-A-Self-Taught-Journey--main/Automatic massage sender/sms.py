#pip install twilio

from twilio.rest import Client
import schedule
import time

# Twilio credentials (replace with your own)
ACCOUNT_SID = "your_account_sid"
AUTH_TOKEN = "your_auth_token"
FROM_PHONE = "+1234567890"  # Twilio phone number
TO_PHONE = "+0987654321"  # Recipient phone number

client = Client(ACCOUNT_SID, AUTH_TOKEN)

def send_sms():
    message = client.messages.create(
        body="Hello! This is an automated message.",
        from_=FROM_PHONE,
        to=TO_PHONE
    )
    print(f"Message sent: {message.sid}")

# Schedule to send every day at 10:00 AM
schedule.every().day.at("10:00").do(send_sms)

while True:
    schedule.run_pending()
    time.sleep(1)
