from django.shortcuts import render, redirect
from accounts.models import CustomUser
from .models import Chat, Message
# Create your views here.

def chat(request,user_id):

	user2 = CustomUser.objects.filter(pk=user_id).first()
	chat = Chat.objects.filter(users=request.user).filter(users=user2).distinct().first()
	chats = Chat.objects.filter(users=request.user)
	if chat == None:
		chat = Chat()
		chat.save()
		chat.users.add(request.user, user2)
	if request.method == 'POST':
		message = Message(chat=chat, content=request.POST.get('content'), sender=request.user)
		message.save()
	return render(request, 'chat.html', {'chat' : chat, 'user2' : user2, 'chats' : chats})

def chat_by_id(request,chat_id):
	chat = Chat.objects.filter(pk=chat_id).first()
	user2 = chat.users.exclude(id=request.user.id).first()
	return redirect('chat', user2.id )

def inbox(request):
	chats = Chat.objects.filter(users=request.user)
	return render(request, 'inbox.html', {'chats' : chats})