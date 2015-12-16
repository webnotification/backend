from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from notification.models import User, Group, User_Group
import random


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
    return HttpResponse("Done!")

def send_notification(request):
    params = request.POST
    website = params['website']
    notification_data = params['notification_data']
    group_id = params['group_id']
    # Add to queue and send
    return HttpResponse("Done!")


