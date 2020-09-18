#!/usr/bin/env python

from config import API_TOKEN

global config

# Enable logging
import logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.WARN)

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests

def welcome_message(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=config.HELLO_MESSAGE)


def display_message(bot, update):
    response = requests.post("https://flipdot.openlab-augsburg.de/api/v2/queue/add",
                             data={
                                 'text': update.message.text
                             })

    bot.send_message(chat_id=update.message.chat_id, text=config.RESPONSE_MESSAGE)


if __name__ == "__main__":
    # HACK: Read Config File
    from importlib.machinery import SourceFileLoader
    config = SourceFileLoader("*", "./config.py").load_module()

    # Create Updater
    updater = Updater(token=config.API_TOKEN)
    dispatcher = updater.dispatcher

    # Register Handlers
    start_handler = CommandHandler('start', welcome_message)
    dispatcher.add_handler(start_handler);

    message_handler = MessageHandler(Filters.text, display_message)
    dispatcher.add_handler(message_handler)

    # Start Bot
    updater.start_polling()
