from __future__ import absolute_import
from celery import shared_task
import requests
import config


@shared_task
def push_notification(title, message, url):
    payload = {
                'title': title,
                'message': message,
                'url': url
            }
    status = requests.post(config.NOTIFICATION_URL, data=payload)
    return 'Sending notification with message: ' + message + str(status)
