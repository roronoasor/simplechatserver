from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_request, name='register'),
    path('login/', views.login, name='login'),
    path('chatinfo/chat_<str:room_name>/', views.chatinfo, name='chatinfo'),
    path('<str:room_name>/', views.room, name='room'),
]