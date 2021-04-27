from . import mail
from flask_mail import Message

def prepare_msg():
    msg = Message('Hello', sender = 'tofutang35728@gmail.com', recipients = ['zushitt@gmail.com'])
    msg.body = "Hello Flask message sent from Flask-Mail"