from spacy.en import English
from parse_date_time import datetime_parser
import configparser
from settings import PROJECT_ROOT
from chatbot.botpredictor import BotPredictor
import os
import tensorflow as tf
from gmail import Gmail
from datetime import datetime
import time
import requests
from threading import Thread

corp_dir = os.path.join(PROJECT_ROOT, 'Data', 'Corpus')
knbs_dir = os.path.join(PROJECT_ROOT, 'Data', 'KnowledgeBase')
res_dir = os.path.join(PROJECT_ROOT, 'Data', 'Result')

sess = tf.Session()
predictor = BotPredictor(sess, corpus_dir=corp_dir, knbase_dir=knbs_dir,
                         result_dir=res_dir, result_file='basic')
# A single chat session only
session_id = predictor.session_data.add_session()

config = configparser.ConfigParser()

parser = English(vectors = False)

class Cognition():
    def __init__(self):
      self.user_context_path = 'users/'
      self.user_name = None
      self.episodic_memory = 'config.ini'
      self.last_question = False
      self.last_action = False
      self.user_intent = False
      self.gmail = False

    def initialize_cognition(self):
        #face recognition ---> user_context
        config.read(self.episodic_memory)
        self.user_name = config['User']['Name']
        # gmail login passwd etc.
        g = Gmail()
        g.login(config['Gmail']['Mail'], config['Gmail']['Passwd'])
        self.gmail = g

    def decompose_query(self, query):
        #print (query)
        doc = parser(query)
        if( ('mail' in query.lower() and 'send' in query.lower()) or (('like' not in query.lower() or 'love' not in query.lower()) and 'mail' in query.lower()) ):
            #email(doc, query)
            self.user_intent = 'email'
        elif( ('remind' in query.lower() and 'me' in query.lower()) or ('set' in query.lower() and 'reminder' in query.lower()) ):
            self.user_intent = 'reminder'
        elif( query.strip() == 'exit' or query.strip() == 'Exit' ):
            self.user_intent = 'exit'
        else:
            self.user_intent = 'chat'
        #executive_functions(query)
        return


class Perception():
    def __init__(self):
      self.user_context_path = 'users/'
      self.reminders = os.path.join(PROJECT_ROOT, 'reminders.txt')
      self.user_id = None
      self.bot = None
    #initiate face_recognition

class Motor_Skills():
    #add send_mail function

   def __init__(self, gmail):
      self.before = False
      self.after = False
      self.on = False
      self.label = False
      self.read = False
      self.starred = False
      self.subject = False
      self.sender = []
      self.to = False
      self.body = False
      self.inbox = 'INBOX'
      self.gmail = gmail

   def parse_mail(self, mail_body):
      body = str(mail_body,'utf-8').replace('\r', '')
      body = body.replace('\n\n', '\n').replace('\n\n', '\n')
      return body
      

   def read_mail(self):
      if( self.inbox == 'starred' ):
         emails = self.gmail.starred().mail(read = self.read, on = self.on, sender = self.sender, subject = self.subject, before = self.before, label = self.label, after = self.after, to = self.to, body = self.body)
      elif( self.inbox == 'important' ):
         emails = self.gmail.important().mail(read = self.read, on = self.on, sender = self.sender, subject = self.subject, before = self.before, label = self.label, after = self.after, to = self.to, body = self.body)
      elif( self.inbox == 'sent' ):
         emails = self.gmail.sent_mail().mail(read = self.read, on = self.on, subject = self.subject, before = self.before, label = self.label, after = self.after, to = self.to, body = self.body)
      elif( self.inbox == 'spam' ):
         emails = self.gmail.spam().mail(read = self.read, on = self.on, sender = self.sender, subject = self.subject, before = self.before, label = self.label, after = self.after, to = self.to, body = self.body)
      else:
         emails = self.gmail.inbox().mail(read = self.read, on = self.on, sender = self.sender, subject = self.subject, before = self.before, label = self.label, after = self.after, to = self.to, body = self.body)

      email_list = []
      for e in emails[:10]:
         e.fetch()
         if (inbox == 'sent'):
            mail_address = e.to
         else:
            mail_address = e.fr
         timestamp = e.sent_at
         mail_tuple = (mail_address, timestamp, parse_mail(e.body))
         email_list.append(mail_tuple)
      return email_list

   def set_reminder(self, message, time):
      with open(self.reminders, 'a') as f:
         f.write('|'.join([message, time, 'not_performed']) + '\n')
      return

class Emotion():
    def __init__(self):
      self.nice_value = False

class Language():
    def __init__(self, predictor, session_id):
      self.sess_id = session_id
      self.reply = predictor.predict

    def respond(self, user_response):
        return self.reply(self.sess_id, user_response)

class Brain(Cognition, Emotion, Perception, Motor_Skills, Language):
    def __init__(self, cognition, emotion, perception, motor_skills, language):
        self.sess_id = language.sess_id
        self.reply = language.reply
        # Motor Skills
        self.before = motor_skills.before
        self.after = motor_skills.after
        self.on = motor_skills.on
        self.label = motor_skills.label
        self.read = motor_skills.read
        self.starred = motor_skills.starred
        self.subject = motor_skills.subject
        self.sender = motor_skills.sender
        self.to = motor_skills.to
        self.body = motor_skills.body
        self.inbox = motor_skills.inbox
        self.gmail = motor_skills.gmail
        self.send = 'no'
        # Cognition
        self.user_context_path = cognition.user_context_path
        self.user_name = cognition.user_name
        self.episodic_memory = cognition.episodic_memory
        self.last_question = cognition.last_question
        self.last_action = cognition.last_action
        self.user_intent = cognition.user_intent
        # Perception
        self.user_id = perception.user_id
        self.bot = perception.bot
        self.reminders = perception.reminders
        # Brain
        self.bot_response = None
        self.initiate_termination = False
        self.voice = {
            'Papaya_Bot' : "'ko-KR'",
            'Indian_Papayee' : "'hi-IN'"
            }
        self.task_pool = Thread(target = self.reminder)
        self.task_pool.start()

    def speech_hack(self, speech_file, token, update_token):
        with open(speech_file) as f:
            s = f.read()
        with open(speech_file, 'w') as f:
            f.write(s.replace(token, update_token))
        return

    def say(self, voice, text):
        print (text)
        speaker = self.voice[voice]
        #speaker['INPUT_TEXT'] = self.bot_response
        speaker_script = os.path.join(PROJECT_ROOT, 'web_speech', 'script.js')
        speaker_file = os.path.join(PROJECT_ROOT, 'web_speech', 'test.html')
        self.speech_hack(speaker_script, "'speaker_voice_token'", speaker)
        self.speech_hack(speaker_file, "'speaker_voice_token'", '"'+text+'"')
        os.system('sh /media/anurag/Other\ Stuff/assistants/chatbot_new/web_speech/chrome_voice.sh')
        time.sleep(5)
        self.speech_hack(speaker_script, speaker, "'speaker_voice_token'")
        self.speech_hack(speaker_file, '"'+text+'"', "'speaker_voice_token'")
        return

    def reminder(self):
        while self.initiate_termination == False:
            with open(self.reminders) as f:
                reminder_notes = f.readlines()
            for reminder in reminder_notes:
                reminder_message, reminder_time, action = reminder.replace('\n', '').split('|')
                if(action == 'not_performed'):
                    reminder_datetime = datetime.strptime(reminder_time, '%Y-%m-%d %H:%M:%S')
                    if(datetime.now() > reminder_datetime):
                        #initiate independent response mechanism
                        if(reminder_message == 'Default'):
                            self.push_message('Hey! Do what you were going to!')
                        else:
                            self.push_message(reminder_message)
                        #keep history of past reminders?
                        reminder_notes.remove(reminder)
            with open(self.reminders, 'w') as f:
                for r in reminder_notes:
                    f.write(r)
            time.sleep(10)
        return


    def parse_timestamp(self, timestamps):
        stamps = []
        if len(timestamps) == 0:
            return []
        else:
            for keyword, dt, _ in timestamps:
                stamps.append(dt)
            stamps.sort()
            return stamps

    def parse_time_query(self, doc, query):
        time_query = query
        for word in doc:
            if (word.pos_ == 'X'):
                time_query = time_query.replace(word.orth_, '')
        return time_query

    def papaya_mail(self, query):
        doc = parser(query)
        timestamp = []
##        before = None
##        after = None
##        on = None
##        sender = []
##        unread = None
##        send = 'no'
##        inbox = 'INBOX'
        _before = ['to', 'before', 'till']
        _after = ['from', 'after', 'since']
        time_query = self.parse_time_query(doc, query)
        timestamp = self.parse_timestamp(datetime_parser(time_query))
        for word in doc:
            if( word.pos_ == 'PROPN' or word.pos_ == 'X' ):
                self.sender.append(word.orth_)
            if( word.pos_ == 'ADP' and len(timestamp) == 1 ):
                if( word.orth_ in _before ):
                    self.before = timestamp[0]
                elif( word.orth_ in _after ):
                    self.after = timestamp[0]
                else:
                    self.on = timestamp[0]
            if( word.pos_ == 'VERB' and word.orth_.lower() in ['send', 'email', 'mail'] ):
                self.send = 'yes'
            if( word.pos_ == 'VERB' and word.orth_.lower() in ['sent'] ):
                self.inbox = 'sent'
            if( word.pos_ == 'VERB' and word.orth_.lower() in ['starred'] ):
                self.inbox = 'starred'
            if( word.pos_ == 'ADJ' and word.orth_.lower() in ['important'] ):
                self.inbox = 'important'
            if( word.pos_ == 'ADJ' and word.orth_.lower() in ['new', 'unread'] ):
                self.unread = 'yes'
            if( word.pos_ == 'VERB' and word.orth_.lower() in ['miss'] ):
                self.unread = 'yes'
            if( word.pos_ == 'NOUN' and word.orth_.lower() in ['sentbox'] ):
                self.inbox = 'sent'
            if( word.pos_ == 'NOUN' and word.orth_.lower() in ['spam', 'spambox'] ):
                self.inbox = 'spam'
        if(len(timestamp) == 2):
            self.before = timestamp[1]
            self.after = timestamp[0]
        if(self.inbox == 'sent'):
            self.to = self.sender
        if(self.send == 'yes'):
            self.gmail.send_mail(self.sender, 'Papaya Mail!!', 'Example Text')
            self.bot_response = "Sending the mail to " + self.sender[0] + ", Just a mo'..."
            self.send = 'no'
        else:
            self.bot_response = "Getting your mail... Be back in a moment..."
            self.push_message("Getting your mail... Be back in a moment...")
            emails = self.read_mail()
            self.bot_response = emails
        #print ('inbox:', inbox, 'before:', before, 'after:', after, 'on:', on, 'unread:', unread, 'sender:', sender, 'send?:', send)
        return

    def push_message(self, message_text):
        self.bot.send_message(chat_id = self.user_id.message.chat_id, text = message_text)
        return

    def reminder_message(self, extracted_datetime, base_date, remind_message):
        if(remind_message == 'Default'):
            time_diff = extracted_datetime - base_date
            time_diff = divmod(time_diff.days * 86400 + time_diff.seconds, 60)
            if(time_diff[0] > 1600):
                self.bot_response = "I'll remind you at " + extracted_datetime.strftime('%Y-%m-%d %H:%M:%S').split(' ')[1] #parse
            else:
                self.bot_response = "I'll remind you at " + extracted_datetime.strftime('%Y-%m-%d %H:%M:%S').split('-', 1)[1] #parse
        else:
            time_diff = extracted_datetime - base_date
            time_diff = divmod(time_diff.days * 86400 + time_diff.seconds, 60)
            if(time_diff[0] > 1600):
                self.bot_response = "I'll remind you at " + extracted_datetime.strftime('%Y-%m-%d %H:%M:%S').split(' ')[1] + " to " + reminder_message #parse
            else:
                self.bot_response = "I'll remind you at " + extracted_datetime.strftime('%Y-%m-%d %H:%M:%S').split('-', 1)[1] + " to " + reminder_message #parse

    def papaya_central(self, query, bot, update):
        self.user_id = update
        self.bot = bot
        if self.user_intent == 'exit':
            self.bot_response = "Ciao!"
            sess.close()
            self.gmail.logout()
            self.initiate_termination = True
            print ('Closing the TF Session')
        elif( self.user_intent == 'chat' ):
            self.last_action = 'chat'
            self.bot_response = self.respond(query)
            self.say('Indian_Papayee', self.bot_response)
        elif( self.user_intent == 'email' ):
            #self.bot_response = 'Yes, yes You wanna send an Email, I get it.'
            self.last_action = 'email'
            #self.say('Indian_Papayee', self.bot_response)
        elif( self.user_intent == 'reminder' ):
            # Add reminder code
            tagged_text, extracted_datetime, location = datetime_parser(query, base_date = datetime.now())[0]
            reminder_message = query[: location[0] - 1]
            if('remind me to ' in reminder_message.lower()):
                reminder_message = reminder_message.lower().split('remind me to ')
            else:
                reminder_message = 'Default'
            self.reminder_message(extracted_datetime, datetime.now(), reminder_message)
            self.set_reminder(reminder_message, extracted_datetime.strftime('%Y-%m-%d %H:%M:%S'))
            self.last_action = 'reminder'
            self.say('Indian_Papayee', self.bot_response)
        return

class Cortex():
    def wake_up():
        cognition = Cognition()
        cognition.initialize_cognition()
        perception = Perception()
        emotion = Emotion()
        language = Language(predictor, session_id)
        motor_skills = Motor_Skills(cognition.gmail)

        print ('Waking Up....')
        brain = Brain(cognition, emotion, perception, motor_skills, language)
        #print ('returning')
        return brain


        
