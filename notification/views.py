from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from notification.models import User, Group, User_Group, PermissionResponse, NotificationResponse
import random
from django.db.models import Count
from django.db import IntegrityError, DataError
from tasks import push_notification
import requests
import json


def index(request):
    return HttpResponse("Hello, Welcome to our notification homepage.")

def generate_user_id(request):
    website = request.GET.get('website')
    try:
        id = User.objects.latest('id').id + 1
    except User.DoesNotExist:
        id = 0
    user = User(id=id, website=website)
    user.save()
    return JsonResponse({'user_id': id})

def generate_group(request):
    params = request.GET
    website = params['website']
    group_name = params['group_name']
    percentage = int(params['percentage'])
    
    group = Group(name=group_name, website=website)
    group.save()
    group_id = Group.objects.latest('id').id

    user_list = User.objects.filter(website=website).values("id")
    shuffled_user_list = sorted(user_list, key=lambda x: random.random())
    final_user_list = shuffled_user_list[:(len(shuffled_user_list)*percentage)/100]
    for user in final_user_list:
        user_group = User_Group(user_id=user['id'], group_id=group_id)
        user_group.save()
    return JsonResponse({'group_id': group_id})

def get_groups(request):
    params = request.GET
    website = params['website']
    group_objects = Group.objects.filter(website=website)
    groups = [group.name for group in group_objects]
    return JsonResponse({'groups': groups})

def save_push_key(request):
    params = request.POST
    website = params['website']
    # id = params['user_id']
    id = 0
    endpoint = params['subs']
    if endpoint.startswith('https://android.googleapis.com/gcm/send'):
        endpointParts = endpoint.split('/')
        push_key = endpointParts[len(endpointParts) - 1]
    user = User.objects.filter(id=id, website=website)[0]
    user.push_key = push_key
    response = ""
    try:
        user.save()
    except DataError as e:
        response = e.message
    response = HttpResponse(response)
    response["Access-Control-Allow-Origin"] = "*"
    return response

def send_to_gcm(user_id):
    uri = 'https://android.googleapis.com/gcm/send'
    payload = json.dumps({
                'registration_ids': [
                   User.objects.filter(id=user_id)[0].push_key     
                    ]
              })
    headers = {
              'Content-Type': 'application/json',
              'Authorization': 'key=AIzaSyDuYIh8i3e63Wyag2XHwDPrFYTPITZvIQY'
            } 
    requests.post(uri, data=payload, headers=headers)

def send_notification(request):
    params = request.POST  # make it POST
    # website = params['website']
    # group_id = params['group_id']
    title = params['title']
    message = params['message']
    url = params['target_url']
    send_to_gcm(user_id=0)
    # push_notification.delay(title, message, url)
    return JsonResponse({'success': True})

def send_permission_response(request):
    params = request.GET
    user_id = params['user_id']
    action = params['action']
    try:
        permissionresponse = PermissionResponse(user_id=user_id, action=action)
        permissionresponse.save()
        response = {'success': True}
    except IntegrityError:
        response = {'error': 'Permission already set'}
    except Exception as e:
        response = {'error': e}
    return JsonResponse(response)

def send_notification_response(request):
    params = request.GET
    user_id = params['user_id']
    notification_id = params['notification_id']
    action = params['action']
    try:
        notificationresponse = NotificationResponse(user_id=user_id, notification_id=notification_id, action=action)
        notificationresponse.save()
        response = {'success': True}
    except IntegrityError:
        response = {'error': 'Notification Status already set'}
    except Exception as e:
        response = {'error': e.message}
    return JsonResponse(response)

def get_permission_CTR(request):
    params = request.GET
    group_id = params['group_id']
    user_list = User_Group.objects.filter(group_id=group_id).values('user_id')
    user_id_list = [user['user_id'] for user in user_list]
    permission_CTR = PermissionResponse.objects.filter(user_id__in=user_id_list).values('action').annotate(ct=Count('action'))
    response = {'result': list(permission_CTR)}
    return JsonResponse(response)
   
def get_notification_CTR(request):
    params = request.GET
    group_id = params['group_id']
    notification_id = params['notification_id']
    user_list = User_Group.objects.filter(group_id=group_id).values('user_id')
    user_id_list = [user['user_id'] for user in user_list]
    notification_CTR = NotificationResponse.objects.filter(user_id__in=user_id_list, notification_id=notification_id).\
            values('action').annotate(ct=Count('action'))
    response = {'result': list(notification_CTR)}
    return JsonResponse(response)
   

