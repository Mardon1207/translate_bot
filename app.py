
    
from flask import Flask,request
from telegram import Update, Bot
from telegram.ext import CommandHandler,MessageHandler,Dispatcher,Filters,CallbackQueryHandler
from handlers import (start, enuz,forwarding,uzen,adminpanel,translate,admin_command,checking)



TOKEN='6409999814:AAFD0zQHnbSUHA4mc6QU9hCgMGKcLvCCsWQ'
bot=Bot(token=TOKEN)
dp=Dispatcher(bot, None, workers=0)


app=Flask(__name__)
@app.route("",methods=["GET","POST"])
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
    
    