from flask import Flask,request
from telegram import Update, Bot
from telegram.ext import CommandHandler,MessageHandler,Dispatcher,Filters
from main import *

TOKEN="5873498271:AAGbWIyvaojE9RZ7HafEVDn2zfU8CVEJ_IY"
bot=Bot(token=TOKEN)
dp=Dispatcher(bot, None, workers=0)


app=Flask(__name__)
@app.route("/webhook",methods=["GET","POST"])
def main():
    if request.method=="GET":
        return "runing"
    if request.method=="POST":
        body=request.get_json()
        update=Update.de_json(body,bot)
        dp.add_handler(CommandHandler('enuz',enuz))
        dp.add_handler(MessageHandler(Filters.reply,forwarding))
        dp.add_handler(CommandHandler('uzen',uzen))
        dp.add_handler(CommandHandler('start',start))
        dp.add_handler(CallbackQueryHandler(adminpanel, pattern='admin'))
        dp.add_handler(MessageHandler(Filters.text,translate))
        dp.add_handler(CallbackQueryHandler(admin_command, pattern='command'))
        dp.add_handler(CallbackQueryHandler(checking, pattern='check'))
        dp.process_update(update)

        return {"message","ok"}
    
if __name__=="__main__":
    app.run(debug=True)
    
    