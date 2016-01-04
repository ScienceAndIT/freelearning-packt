from __future__ import absolute_import
import requests
from lxml import html
#from random import randint
from django.core.mail import EmailMessage
#from celery import shared_task
from celery.schedules import crontab
from celery.task import periodic_task
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)
params = {'email': 'youremail',
          'password': 'yourpassword',
          'op': 'Login',
          'form_id': 'packt_user_login_form'}
FREE_LEARNING_URL = 'https://www.packtpub.com/packt/offers/free-learning'
PACKT_URL = 'https://www.packtpub.com'
page = requests.get(FREE_LEARNING_URL)
webpage = html.fromstring(page.content)
book_number = webpage.xpath("//a[@class='twelve-days-claim']/@href")
book_title = webpage.xpath("//div[@class='dotd-title']/h2/text()")


@periodic_task(run_every=(crontab(minute=0, hour=8)),
               name='task_grab_free_ebook',
               ignore_result=True
               )
def task_grab_free_ebook():
    # Use 'with' to ensure the session context is closed after use.
    with requests.Session() as s:
        p = s.post(FREE_LEARNING_URL, data=params)
        # An authorised request.
        r = s.get(PACKT_URL + book_number[0])
        # Log out
        l = s.get(PACKT_URL + '/logout')


@periodic_task(run_every=(crontab(minute='*/1')),
               name='task_send_email_about_ebook',
               ignore_result=True
               )
def task_send_email_about_ebook():
    subject = 'Your free e-book from PacktPub has just arrived'
    message = "Your new e-book is - " + book_title[0].strip()
    email = EmailMessage(subject,
                         message,
                         'from@example.com',
                         ['to@example.com'])
    email.content_subtype = "html" # Main content is now text/html
    email.send(fail_silently=True)

"""
@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@periodic_task(run_every=(crontab(minute='*/1')),
               name='task_generate_random_number',
               ignore_result=True
               )
def task_generate_random_number():
    print randint(1, 100)
    logger.info("Random number generated")
"""

