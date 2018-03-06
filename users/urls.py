from django.conf.urls import url
from . import views

app_name = 'users'
urlpatterns = [
    url(r'^register/', views.register, name='register'),
    url(r'^addservice/', views.addservice, name='addservice'),
    url(r'^requireport/', views.requireport, name='requireport')
]
