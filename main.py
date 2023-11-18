from telegram.ext import Updater,CommandHandler,CallbackContext,MessageHandler,Filters,CallbackQueryHandler
from telegram import (
    Bot,Update,ReplyKeyboardMarkup,KeyboardButton,InlineKeyboardMarkup,
    InlineKeyboardButton,ChatAdministratorRights,ParseMode
    )

from deep_translator import GoogleTranslator

from db import DB

bot = Bot('5873498271:AAGbWIyvaojE9RZ7HafEVDn2zfU8CVEJ_IY')
def en_uz(text):
    tr_text = GoogleTranslator(source='en',target='uz').translate(text)
    return tr_text

def uz_en(text):
    tr_text = GoogleTranslator(source='uz',target='en').translate(text)
    return tr_text

def ru_uz(text):
    tr_text = GoogleTranslator(source='ru',target='uz').translate(text)
    return tr_text

def uz_ru(text):
    tr_text = GoogleTranslator(source='uz',target='ru').translate(text)
    return tr_text


def translate(update:Update, context:CallbackContext):
    bot=context.bot 
    chat_id=update.message.chat.id
    text = update.message.text
    db = DB()
    til = db.get_lang(chat_id)
    if til == 'en-uz':
        tr_text = en_uz(text)
    elif til == 'uz-en':
        tr_text = uz_en(text)
    elif til == 'ru-uz':
        tr_text = ru_uz(text)
    else:
        tr_text = uz_ru(text)
    db.save()
    bot.send_message(chat_id, f'`{tr_text}`', parse_mode=ParseMode.MARKDOWN)

def start(update:Update,context:CallbackContext):
    bot=context.bot 
    chat_id=update.message.chat.id
    db = DB()
    a = db.check_admins(chat_id)
    if a:
        btn = InlineKeyboardButton('👤Admin panel', callback_data='admin panel')
        btn1 = InlineKeyboardMarkup([[btn]])
        bot.send_message(chat_id, 'Admin sozlamalari ⚙️', reply_markup=btn1)
    db.starting(chat_id)
    db.save()

def uzen(update:Update,context:CallbackContext):
    bot=context.bot 
    chat_id=update.message.chat.id
    db = DB()
    db.change(chat_id,'uz-en')
    db.save()
    bot.send_message(chat_id,'Tarjima uchun matn kirgizing')

def enuz(update:Update, context:CallbackContext):
    bot=context.bot 
    chat_id=update.message.chat.id
    db = DB()
    db.change(chat_id,'en-uz')
    db.save()
    bot.send_message(chat_id,'Enter text for translation', parse_mode=ParseMode.MARKDOWN)

# def adminpanel(update:Update, context:CallbackContext):

    

updater=Updater('5873498271:AAGbWIyvaojE9RZ7HafEVDn2zfU8CVEJ_IY')

updater.dispatcher.add_handler(CommandHandler('start',start))
updater.dispatcher.add_handler(CommandHandler('uzen',uzen))
updater.dispatcher.add_handler(CommandHandler('enuz',enuz))
updater.dispatcher.add_handler(MessageHandler(Filters.text,translate))

updater.start_polling()
updater.idle()