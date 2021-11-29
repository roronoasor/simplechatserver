from django.db import models

from mongoengine import Document, fields, EmbeddedDocument, EmbeddedDocumentField



class User(Document):
    name = fields.StringField()
    email = fields.StringField()
    password = fields.StringField()

    meta = {'db_alias': 'solbot'}


class Chatroom(Document):
    chatroom = fields.StringField()
    users = fields.ListField()

class chatmessage(Document):
    message = fields.StringField()
    chatroom = fields.StringField()
    username = fields.StringField()
    timestamp = fields.DateTimeField()

