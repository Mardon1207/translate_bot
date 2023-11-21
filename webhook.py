from telegram import Bot

TOKEN="5873498271:AAGbWIyvaojE9RZ7HafEVDn2zfU8CVEJ_IY"

bot = Bot(token=TOKEN)

def get_info():
    print(bot.get_webhook_info())


def delete():
    print(bot.delete_webhook())


def set():
    url = 'https://translatebot.pythonanywhere.com/webhook'
    print(bot.set_webhook(url=url))

set()