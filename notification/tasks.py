from __future__ import absolute_import
from celery import shared_task
import requests
import config
import json
from notification.models import Ask_Permission


@shared_task
def push_notification(user_registration_keys, title, message, url):
    for user_registration_key in user_registration_keys:
        payload = json.dumps({'registration_ids': [user_registration_key['push_key']]})
        headers = {
                  'Content-Type': 'application/json',
                  'Authorization': config.GCM_AUTHORIZATION,
                } 
        requests.post(config.GCM_URL, data=payload, headers=headers)
    return 'Notifications sent'

@shared_task
def push_permission_message(user_list):
    user_list = [user['id'] for user in user_list ]
    ask_permission = Ask_Permission.objects.filter(user_id__in=user_list).update(ask=True)
    return 'Permission messages sent'
