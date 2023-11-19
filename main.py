from telegram.ext import Updater,CommandHandler,CallbackContext,MessageHandler,Filters,CallbackQueryHandler
from telegram import (
    Bot,Update,ReplyKeyboardMarkup,KeyboardButton,InlineKeyboardMarkup,
    InlineKeyboardButton,ChatAdministratorRights,ParseMode
    )

from deep_translator import GoogleTranslator

from db import DB

def tekshir(chat_id,bot,channel):
    chan1=bot.getChatMember(channel,str(chat_id))['status']
    if chan1=='left':
        return False
    return True

bot = Bot('5873498271:AAGbWIyvaojE9RZ7HafEVDn2zfU8CVEJ_IY')
def en_uz(text):
    tr_text = GoogleTranslator(source='en',target='uz').translate(text)
    if tr_text==text:
        tr_text = GoogleTranslator(source='uz',target='en').translate(text)
        return tr_text
    else:
        return tr_text




def translate(update:Update, context:CallbackContext):
    bot=context.bot 
    try:
        chat_id=update.message.chat.id
        message = update.message
        db = DB()
        a = db.check_admins(chat_id)
        msg=False
        addd = False
        remd = False
        addc = False
        removec = False
        if a:
            ruxsat = db.ruxsatlar(chat_id)
            msg = ruxsat['msg']
            addd = ruxsat['addd']
            remd = ruxsat['removed']
            addc = ruxsat['addc']
            removec = ruxsat['removec']
            if msg:
                users = db.allusers()
                if msg:
                    i=0
                    for user in users:
                        try:
                            bot.send_message(f'{user}', message.text)
                            i+=1
                        except:
                            pass
                    bot.send_message(chat_id,f'{i} ta foydalanuvchiga xabar muvafaqiyatli yuborildi')
            elif addd and message.text[:6]=='admin+':
                db.add(message.text[6:],'admin',None)
                try:
                    usr = bot.get_chat(message.text[6:])
                    bot.send_message(chat_id,f'Admin qo\'shildi✅\n\nuser id : {message.text[6:]}\n\nname: {usr.first_name}\n\nusername: {usr.username}')
                except:
                    bot.send_message(chat_id,f'Admin qo\'shildi✅\nUser haqida malumotlar topilmadi')
            elif remd and message.text[:6]=='admin-':
                try:
                    db.delete(message.text[6:])
                    usr = bot.get_chat(message.text[6:])
                    bot.send_message(chat_id,f'Admin o\'chirildi✅\n\nuser id : {message.text[6:]}\n\nname: {usr.first_name}\n\nusername: {usr.username}')
                except:
                    bot.send_message(chat_id,'Admin o\'chirishda xatolik bo\'lishi mumkin tekshirib ko\'ring')
            elif addc and message.text[:8]=='channel+':
                q = db.channel(message.text[8:],'add')
                if q:
                    try:
                        chan1=bot.getChatMember(message.text[8:],chat_id)['status']
                        bot.sendMessage(chat_id,'Chat muvafaqiyatli qo\'shildi✅')
                    except:
                        bot.sendMessage(chat_id,'Kanal qo\'shishda xatolik tekshirib qayta urinib ko\'ring')
                        q=db.channel(message.text[8:],'delete')
            elif removec and message.text[:8]=='channel-':
                q=db.channel(message.text[8:],'delete')
                if q:
                    bot.sendMessage(chat_id,'Kanal muvafaqiyatli o\'chirildi')
                else:
                    bot.sendMessage(chat_id,'Kanal o\'chirishda xatolik')
                
            else:
                text = update.message.text
                tr_text=en_uz(text)
                db.save()
                bot.send_message(chat_id, f'`{tr_text}`', parse_mode=ParseMode.MARKDOWN)
        else:
            text = update.message.text
            tr_text=en_uz(text)
            db.save()
            bot.send_message(chat_id, f'`{tr_text}`', parse_mode=ParseMode.MARKDOWN)
        db.save()
    except:
        pass

def start(update:Update,context:CallbackContext):
    bot=context.bot 
    chat_id=update.message.chat.id
    tp = update.message.chat.type
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

def adminpanel(update:Update, context:CallbackContext):
    query = update.callback_query
    chat_id = query.message.chat_id
    msg = query.message.message_id
    bot=context.bot
    command = query.data.split(' ')[0]
    db = DB()
    a = db.check_admins(chat_id)
    if a:
        btn1 = InlineKeyboardButton('📨Xabar yuborish', callback_data='command sendmsg')
        btn2 = InlineKeyboardButton('📩Forward yuborish', callback_data='command sendfwd')
        btn3 = InlineKeyboardButton('👤Admin qo\'shish', callback_data='command addadmin')
        btn4 = InlineKeyboardButton('📢Kanal qo\'shish', callback_data='command addchannel')
        btn5 = InlineKeyboardButton('👤Admin o\'chirish', callback_data='command dltadmin')
        btn6 = InlineKeyboardButton('📢Kanal o\'chirish', callback_data='command dltchannel')
        btn7 = InlineKeyboardButton('📄Admin va kanallar', callback_data='command list')
        btn8 = InlineKeyboardButton('📊Statistika', callback_data='command statistik')
        btn = InlineKeyboardMarkup([[btn1,btn2],[btn3,btn4],[btn5,btn6],[btn7],[btn8]])
        bot.delete_message(chat_id=chat_id, message_id=msg)
        bot.sendMessage(chat_id, '*Admin menu*', reply_markup=btn, parse_mode=ParseMode.MARKDOWN)
    else:
        bot.sendMessage(chat_id, 'Bad request')
    db.save()

def admin_command(update:Update, context:CallbackContext):
    query = update.callback_query
    chat_id = query.message.chat_id
    msg = query.message.message_id
    bot=context.bot
    command = query.data.split(' ')[1]
    db = DB()
    a = db.check_admins(chat_id)
    bot.delete_message(chat_id=chat_id, message_id=msg)
    if a:
        db.rmsg(chat_id,False)
        db.rfwd(chat_id,False)
        db.changer(chat_id,'addd')
        db.changer(chat_id,'addc')
        db.changer(chat_id,'removed')
        db.changer(chat_id,'removec')
        if command == 'sendmsg':
            db.rmsg(chat_id,True)
            bot.send_message(chat_id=chat_id, text='Barcha foydalanuvchilarga yuborish uchun text xabar yozing')
        elif command == 'sendfwd':
            db.rfwd(chat_id,True)
            bot.send_message(chat_id,'Barcha foydalanuvchilarga *Forward message* yuborish uchun xabarni ulashing',parse_mode=ParseMode.MARKDOWN)
        elif command == 'addadmin':
            db.changer(chat_id,'addd',True)
            bot.send_message(chat_id=chat_id, text="Yangi admin qo'shish uchun user_idisini quyidagicha kiriting:\n\nadmin+user_id")
        elif command == 'dltadmin':
           db.changer(chat_id,'removed',True) 
           bot.send_message(chat_id=chat_id, text="Adminni o'cirish uchun user_idisini quyidagicha kiriting:\n\nadmin-user_id") 
        elif command == 'addchannel':
            db.changer(chat_id,'addc',True)
            bot.send_message(chat_id=chat_id, text="Botga majburiy obuna qo'shish uchun birinchi navbatda botni kanalga dmin qiling va quyidagicha kiriting kanal usernameni:\n\nchannel+username")
        elif command == "dltchannel":
            db.changer(chat_id,'removec',True)
            bot.send_message(chat_id=chat_id, text="Majburiy obuna ro'yxatidan kanalni chiqarib tashlash uchun quyidagicha kiriting kanal usernameni:\n\nchannel-username")
        elif command == 'list':
            channels = db.channels()
            if len(channels)!=0:
                text = 'Majburiy obuna uchun kanallar:\n'
                for channel in channels:
                    text+=f'*{channel}*\n'
                bot.sendMessage(chat_id,text,parse_mode=ParseMode.MARKDOWN)
            else:
                bot.sendMessage(chat_id,'Majburiy obuna uchun hech narsa topilmadi',parse_mode=ParseMode.MARKDOWN)
            admins = db.alladmins()
            text = 'Adminlar:\n\n'
            for admin in admins:
                try:
                    usr = bot.get_chat(admin)
                    text += f'User id: `{usr.id}`\nname: `{usr.first_name}`\nusername: `{usr.username}`\n\n'
                except:
                    text += f'User id: `{admin}`'
            bot.sendMessage(chat_id,text,parse_mode=ParseMode.MARKDOWN)
    db.save()

            

updater=Updater('5873498271:AAGbWIyvaojE9RZ7HafEVDn2zfU8CVEJ_IY')

updater.dispatcher.add_handler(CommandHandler('start',start))
updater.dispatcher.add_handler(CommandHandler('uzen',uzen))
updater.dispatcher.add_handler(CommandHandler('enuz',enuz))
updater.dispatcher.add_handler(CallbackQueryHandler(adminpanel, pattern='admin'))
updater.dispatcher.add_handler(MessageHandler(Filters.text,translate))
updater.dispatcher.add_handler(CallbackQueryHandler(admin_command, pattern='command'))

updater.start_polling()
updater.idle()