import random
import string
from flask_mail import Message
from extensions import mail


def send_email(application, to, from_email, subject, body):
    with application.app_context():
        msg = Message(subject, sender=from_email, recipients=[to])
        msg.body = body
        mail.send(msg)
        return True


def generate_code(length=15):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))
