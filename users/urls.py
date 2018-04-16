from django.conf.urls import url
from . import views

app_name = 'users'
urlpatterns = [
    url(r'^register/', views.register, name='register'),
    url(r'^service_list/', views.service_list, name='service_list'),
    url(r'^user_center/', views.user_center, name='user_center'),
    url(r'^get_order_info/', views.get_order_info, name='get_order_info'),
    url(r'^get_auth_obj/',views.get_auth_obj, name='get_auth_obj')
]
