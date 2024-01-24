from telegram import Bot

TOKEN="6433158894:AAHJfMA9JLUOHT5C-AVvZS0UQGUJNVUEFhs"

bot = Bot(token=TOKEN)

def get_info():
    print(bot.get_webhook_info())


def delete():
    print(bot.delete_webhook())

delete()
def set():
    url = 'https://shaxzod03.pythonanywhere.com/webhook'
    print(bot.set_webhook(url=url))

