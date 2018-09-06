import os
import sys
#import tensorflow as tf
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

def echo(user_response):
    """Echo the user message."""
    #global sess
    #user_response = update.message.text
    #print ('# ', user_response)
    brain.decompose_query(user_response)
    brain.papaya_central(user_response)
    if brain.user_intent == 'exit':
        print ('> ', brain.bot_response)
        #brain.say('Papaya_Bot')
    elif( brain.user_intent == 'chat' ):
        print ('> ', brain.bot_response)
        #brain.say('Papaya_Bot')
    elif( brain.user_intent == 'email' ):
        brain.papaya_mail(user_response)
        # Call read_mail/send_mail
        #brain.say('Papaya_Bot')
        print ('> ', brain.bot_response)
    elif( brain.user_intent == 'reminder' ):
        print ('> ', brain.bot_response)
        #brain.say('Papaya_Bot')
    return
    

"""Start the bot."""
print ('Initialization Complete...')

question = ''
while True:
    question = str(input('# '))#sys.stdin.readline()
    if question.strip() == 'exit':
        echo(question)
        break
    else:
        echo(question)

# Run the bot until you press Ctrl-C or the process receives SIGINT,
# SIGTERM or SIGABRT. This should be used most of the time, since
# start_polling() is non-blocking and will stop the bot gracefully.


