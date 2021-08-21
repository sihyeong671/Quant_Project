import string
import random
import threading

from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from django.core.management.utils import get_random_secret_key


class EmailThread(threading.Thread):
    def __init__(self, subject, message, from_email, recipient_list,
              fail_silently, html):
        self.subject = subject
        self.message = message
        self.from_email = from_email
        self.recipient_list = recipient_list
        self.fail_silently = fail_silently
        self.html = html
        threading.Thread.__init__(self)
    
    def run(self):
        print(self.recipient_list)
        msg = EmailMultiAlternatives(
            self.subject, self.message, self.from_email, to=self.recipient_list)
        if self.html:
            msg.attach_alternative(self.html, "text/html")
        msg.send(self.fail_silently)


def send_mail(subject, recipient_list, message='', 
              from_email=settings.EMAIL_HOST_USER,
              fail_silently=False, html=None, *args, **kwargs):
    EmailThread(
        subject, message, from_email, recipient_list, fail_silently, html
        ).start()


def email_auth_string():
    LENGTH = 12
    string_pool = string.ascii_letters + string.digits
    auth_string = ""
    
    for i in range(LENGTH):
        auth_string += random.choice(string_pool)
    
    return auth_string