"""Simple Bot to reply to Telegram messages.

This Bot uses the Updater class to handle the bot.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import os
import sys
#import tensorflow as tf
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

from papaya_brain_lateralized import Cortex

brain = Cortex.wake_up()

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'



#brain.initiate_cognition(predictor, session_id)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(bot, update):
    """Echo the user message."""
    #global sess
    user_response = update.message.text
    print ('# ', user_response)
    brain.decompose_query(user_response)
    brain.papaya_central(user_response, bot, update)
    if brain.user_intent == 'exit':
        print ('> ', brain.bot_response)
        #brain.say('Papaya_Bot')
        update.message.reply_text(brain.bot_response)
    elif( brain.user_intent == 'chat' ):
        print ('> ', brain.bot_response)
        #brain.say('Papaya_Bot')
        update.message.reply_text(brain.bot_response)
    elif( brain.user_intent == 'email' ):
        brain.papaya_mail(user_response)
        # Call read_mail/send_mail
        if(type(brain.bot_response) is list):
            bot_response = '\n\n'.join(brain.bot_response)
            print ('> ', brain.bot_response)
            update.message.reply_text(brain.bot_response)
        else:
            print ('> ', brain.bot_response)
            update.message.reply_text(brain.bot_response)
    elif( brain.user_intent == 'reminder' ):
        print ('> ', brain.bot_response)
        #brain.say('Papaya_Bot')
        update.message.reply_text(brain.bot_response)
    


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


# Waiting from standard input.
##sys.stdout.write("> ")
##sys.stdout.flush()
##question = sys.stdin.readline()

##while question:
##    if question.strip() == 'exit':
##        print("Ciao!")
##        break
##
##    print(predictor.predict(session_id, question))
##    print("> ", end="")
##    sys.stdout.flush()
##    question = sys.stdin.readline()

"""Start the bot."""
# Create the EventHandler and pass it your bot's token.
updater = Updater("***********************************************")

# Get the dispatcher to register handlers
dp = updater.dispatcher

# on different commands - answer in Telegram
dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("help", help))

# on noncommand i.e message - echo the message on Telegram
dp.add_handler(MessageHandler(Filters.text, echo))

# log all errors
dp.add_error_handler(error)

# Start the Bot
updater.start_polling()

print ('Initialization Complete...')

# Run the bot until you press Ctrl-C or the process receives SIGINT,
# SIGTERM or SIGABRT. This should be used most of the time, since
# start_polling() is non-blocking and will stop the bot gracefully.
updater.idle()


