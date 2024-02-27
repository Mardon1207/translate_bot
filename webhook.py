from telegram import Bot

TOKEN="6031625012:AAFdxBk9YBo_m2U4llpFUk854ZoLXTPWSZ0"

bot = Bot(token=TOKEN)

def get_info():
    print(bot.get_webhook_info())


def delete():
    print(bot.delete_webhook())

delete()
def set():
    url = 'https://mardon12.pythonanywhere.com/webhook'
    print(bot.set_webhook(url=url))

set()