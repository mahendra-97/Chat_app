from django.urls import path
from .views import chat_list, chat_room, signup

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('', chat_list, name='chat_list'),
    path('chat/<str:username>/', chat_room, name='chat_room'),
]
