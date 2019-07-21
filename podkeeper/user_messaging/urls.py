from django.urls import path
from django.conf.urls import url
from . import views



urlpatterns = [
  path('chat/<int:user_id>', views.chat, name='chat'),
  path('chatid/<int:chat_id>', views.chat_by_id, name='chat_by_id'),
  path('inbox', views.inbox, name="inbox"),

]