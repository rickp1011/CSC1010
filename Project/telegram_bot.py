link = 'https://api.telegram.org/bot5116787822:AAGMxhOJb6esbb2rcAmAk-QgNm15ukXtDss/getUpdate'
chatID = '0'

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

def start(update: Update,callback:CallbackContext):
    global chatID
    chatID = update.message.chat.id
    updater.bot.send_message(chatID,text='Initializing Bot\nThank you for using pet water bottle!')
    updater.bot.send_message(chatID,'Chat ID: '+ str(chatID))

def send():
    updater.bot.send_message(chatID,text='Good morning!')

def sendUpdateNotif():
    updater.bot.send_message(chatID,'Warning low water warning!')

updater = Updater('5116787822:AAGMxhOJb6esbb2rcAmAk-QgNm15ukXtDss')

updater.dispatcher.add_handler(CommandHandler('start', start))

updater.start_polling()
updater.idle()

