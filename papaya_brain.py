from spacy.en import English
from parse_date_time import datetime_parser

parser = English(vectors = False)

class Brain():
    def __init__(self):
      self.last_action = False
      self.user_intent = False
      self.last_question = False

    def decompose_query(self, query):
        print (query)
        doc = parser(query)
        if( (('mail' and 'send') in query.lower()) or (('like' or 'love') not in query.lower() and 'mail' in query.lower()) ):
            #email(doc, query)
            self.user_intent = 'email'
        elif( ('remind' and 'me') in query.lower() or ('set' and 'reminder') in query.lower()):
            self.user_intent = 'reminder'
        elif( query.strip() == 'exit' ):
            self.user_intent = 'exit'
        else:
            self.user_intent = 'chat'
        return

class Papaya_Mail():

   def __init__(self, gmail):
      self.before = False
      self.after = False
      self.on = False
      self.label = False
      self.read = False
      self.starred = False
      self.subject = False
      self.sender = False
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
