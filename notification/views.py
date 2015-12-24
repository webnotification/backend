from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from notification.models import User, Group, Notification, Permission, PermissionResponse, NotificationResponse, Ask_Permission, Notification_Queue
from django.db.models import Count
from django.db import IntegrityError, DataError
from tasks import push_notification, push_permission_message
import requests
import json
import random


def index(request):
    return HttpResponse("Hello, Welcome to our notification homepage.")

def generate_user_id(request):
    website = request.GET['website']
    try:
        id = User.objects.latest('id').id + 1
    except User.DoesNotExist:
        id = 0
    user = User(id=id, website=website)
    user.save()
    ask_permission = Ask_Permission(user_id=id, ask=False)
    ask_permission.save()
    response = {'user_id': id}
    response = JsonResponse(response)
    response["Access-Control-Allow-Origin"] = "*"
    return response

def generate_group(request):
    params = request.GET
    website = params['website']
    group_name = params['group_name']
    percentage = int(params['percentage'])
    response = {'success': True}
    try:
        group = Group(name=group_name, website=website, percentage=percentage)
        group.save()
    except Exception as e:
        response = {'error': str(e.__class__.__name__)}
    return JsonResponse(response)

def delete_group(request):
    params = request.GET
    website = params['website']
    group_name = params['group_name']
    response = {'success': True}
    try:
        group = Group.objects.filter(name=group_name, website=website)
        group.delete()
    except Exception as e:
        response = {'error': e.message}
    return JsonResponse(response)

def get_groups(request):
    params = request.GET
    website = params['website']
    group_objects = Group.objects.filter(website=website)
    groups = [{'group_name': group.name, 'percentage': group.percentage} for group in group_objects]
    return JsonResponse({'groups': groups})

def save_push_key(request):
    params = request.POST
    website = params['website']
    user_id = params['user_id']
    endpoint = params['subs']
    if endpoint.startswith('https://android.googleapis.com/gcm/send'):
        endpointParts = endpoint.split('/')
        push_key = endpointParts[len(endpointParts) - 1]
    user = User.objects.filter(id=user_id, website=website)[0]
    user.push_key = push_key
    response = {'sucess': True}
    try:
        user.save()
    except DataError as e:
        response = {'error': e.message}
    response = JsonResponse(response)
    response["Access-Control-Allow-Origin"] = "*"
    return response

def get_notification_user_list(website, group_name):
    percentage = Group.objects.filter(name=group_name)[0].percentage
    user_list = User.objects.filter(website=website).exclude(push_key=u'').values("id", "push_key")   
    shuffled_user_list = sorted(user_list, key=lambda x: random.random())
    final_user_list = shuffled_user_list[:(len(shuffled_user_list)*percentage)/100]
    return final_user_list

def get_permission_user_list(website, group_name):
    percentage = Group.objects.filter(name=group_name)[0].percentage
    user_list = User.objects.filter(website=website, push_key=u'').values("id")   
    shuffled_user_list = sorted(user_list, key=lambda x: random.random())
    final_user_list = shuffled_user_list[:(len(shuffled_user_list)*percentage)/100]
    return final_user_list

def send_notification(request):
    # import  ipdb
    # ipdb.set_trace()
    params = request.POST  
    website = params['website']
    group_name= params['group_name']
    title = params['title']
    message = params['message']
    target_url = params['target_url']
    notification = Notification(title=title, message=message, target_url=target_url)
    notification.save()
    notification_id = notification.id
    user_list = get_notification_user_list(website, group_name)
    push_notification.delay(user_list, title, message, target_url, notification_id)
    return JsonResponse({'success': True})

def get_notification_data(request):
    params = request.GET
    user_id = params['user_id']
    notification_id = Notification_Queue.objects.filter(user_id=user_id)[0].notification_id
    notification = Notification.objects.get(id=notification_id)
    notification_data = {
                        'title': notification.title,
                        'message': notification.message,
                        'target_url': notification.target_url
            }
    Notification_Queue.objects.filter(notification_id=notification_id, user_id=user_id).delete()
    response = JsonResponse(notification_data)
    response["Access-Control-Allow-Origin"] = "*"
    return response

def send_permission_message(request):
    params = request.POST
    website = params['website']
    group_name = params['group_name']
    permission = Permission()
    permission.save()
    permission_id = permission.id
    user_list = get_permission_user_list(website, group_name)
    push_permission_message.delay(user_list, permission_id) 
    return JsonResponse({'success': True})

def ask_permission(request):
    params = request.GET
    user_id = params['user_id']
    ask_permission = Ask_Permission.objects.get(user_id=user_id)
    permission_data = {
                'ask': ask_permission.ask,
                'permission_id': ask_permission.permission_id
            }
    response  = JsonResponse(permission_data)
    response["Access-Control-Allow-Origin"] = "*"
    return response
    
def send_permission_response(request):
    params = request.POST
    user_id = params['user_id']
    permission_id = params['permission_id']
    action = params['action']
    try:
        permissionresponse = PermissionResponse(user_id=user_id, permission_id=permission_id, action=action)
        permissionresponse.save()
        response = {'success': True}
    except IntegrityError:
        response = {'error': 'Permission already set'}
    except Exception as e:
        response = {'error': e}
    return JsonResponse(response)

def send_notification_response(request):
    params = request.POST
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
    permission_id = params['permission_id']
    permission_CTR = PermissionResponse.objects.filter(permission_id=permission_id).values('action').annotate(count=Count('action'))
    response = {'result': list(permission_CTR)}
    return JsonResponse(response)
   
def get_notification_CTR(request):
    params = request.GET
    notification_id = params['notification_id']
    notification_CTR = NotificationResponse.objects.filter(notification_id=notification_id).values('action').annotate(count=Count('action'))
    response = {'result': list(notification_CTR)}
    return JsonResponse(response)

