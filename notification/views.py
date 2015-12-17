from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from notification.models import User, Group, User_Group, PermissionResponse, NotificationResponse
import random
from django.db.models import Count
from django.db import IntegrityError

def index(request):
    return HttpResponse("Hello, Welcome to our notification homepage.")

def generate_user_id(request):
    website = request.GET.get('website', '')
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

def save_push_key(request):
    params = request.POST
    website = params['website']
    id = params['user_id']
    push_key = params['push_key']
    user = User.objects.filter(id=id, website=website)[0]
    user.push_key = push_key
    user.save()
    return JsonResponse({'success': True})

def send_notification(request):
    params = request.POST
    website = params['website']
    notification_data = params['notification_data']
    group_id = params['group_id']
    # Add to queue and send
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
   

