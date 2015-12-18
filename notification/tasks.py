from __future__ import absolute_import

from celery import shared_task

@shared_task
def push_notification(message):
    return 'Sending notification with message: ' + message
