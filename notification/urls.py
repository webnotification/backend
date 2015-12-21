from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^generate_user_id$', views.generate_user_id, name='generate_user_id'),
    url(r'^generate_group$', views.generate_group, name='generate_group'),
    url(r'^save_push_key$', views.save_push_key, name='save_push_key'),
    url(r'^send_notification$', views.send_notification, name='send_notification'),
    url(r'^send_permission_response$', views.send_permission_response, name='send_permission_response'),
    url(r'^send_notification_response$', views.send_notification_response, name='send_notification_response'),
    url(r'^get_permission_CTR$', views.get_permission_CTR, name='get_permission_CTR'),
    url(r'^get_notification_CTR$', views.get_notification_CTR, name='get_notification_CTR'),
]
