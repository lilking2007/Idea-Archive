#pip install python-telegram-bot

from telegram import Bot
import schedule
import time

bot = Bot(token="your_bot_token")
chat_id = "your_chat_id"

def send_telegram_message():
    bot.send_message(chat_id=chat_id, text="Hello! This is an automated message.")
    print("Message sent on Telegram!")

schedule.every().day.at("14:00").do(send_telegram_message)

while True:
    schedule.run_pending()
    time.sleep(1)
