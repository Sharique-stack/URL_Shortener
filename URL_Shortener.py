import requests
from telegram import *
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters, PreCheckoutQueryHandler, ShippingQueryHandler
import telegram
import logging

import os
PORT = int(os.environ.get('PORT', 3000))
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)
TOTAL_USERS = []
Admin_Chat_ID = 1067277106
url = "https://url-shortener-service.p.rapidapi.com/shorten"

payload = "url=https%3A%2F%2Fgoogle.com%2F"
headers = {
    'content-type': "application/x-www-form-urlencoded",
    'x-rapidapi-host': "url-shortener-service.p.rapidapi.com",
    'x-rapidapi-key': "fe6f1a9712msh8e2e229380991ffp1378a7jsn853547c696c5"
    }


# ----------------------------------------------------------------------------------------

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(text='Welcome to URL Shortener!\nPlease provide a valid url')
    context.bot.send_message(chat_id=Admin_Chat_ID,
                             text=f'✅ @{update.effective_user.username} started the bot!')

def edit_message_text(context, chat_id, message_id,text):
    context.bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text=text)

def shorten_url(update: Update, context: CallbackContext, url, msg):
    try:
        url = "https://url-shortener-service.p.rapidapi.com/shorten"
        response = requests.request("POST", url, data=payload, headers=headers)
        urlJson = response.json()
        return urlJson['result_url']

    except:
        return False

def TextHandler(update: Update, context: CallbackContext) -> None:
    text = str(update.message.text)
    list_1 = [MessageEntity.URL]

    if update.message.parse_entities(types=list_1):

        msg = update.message.reply_text(text='🔗 Shortening the URL...', quote=True)
        data = shorten_url(update, context, text, msg)
        if data == False:
            update.message.reply_text(text='Sorry I could not process this URL!', quote=True)
            return
        try:
            edit_message_text(context=context,
                              chat_id=update.effective_user.id,
                              message_id=msg.message_id,
                              text=f'Your shortened URL 🔗: {data}\n\n@anyShortenerBot')

        except:
            edit_message_text(context=context,
                              chat_id=update.effective_user.id,
                              message_id=msg.message_id,
                              text=f'Your shortened URL is: {data}')

    else:
        update.message.reply_text(text='Sorry I could not process this URL!', quote=True)


@run_async
def main():
    TOKEN = "5119135849:AAGkTLY6_V-UeMhfEQKwF0A0DnP-IespCAw"
    APP_NAME = 'https://urlshortenerbot1.herokuapp.com/'

    updater = Updater(TOKEN, use_context=True)
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(MessageHandler(Filters.all & ~Filters.command, TextHandler, run_async=True))
    updater.start_polling()
    updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN, webhook_url=APP_NAME + TOKEN)


if __name__ == '__main__':
    main()
