from telegram import Bot

TOKEN="6409999814:AAFD0zQHnbSUHA4mc6QU9hCgMGKcLvCCsWQ"

bot = Bot(token=TOKEN)

def get_info():
    print(bot.get_webhook_info())


def delete():
    print(bot.delete_webhook())


def set():
    url = 'http://127.0.0.1:5000/webhook'
    print(bot.set_webhook(url=url))

set()