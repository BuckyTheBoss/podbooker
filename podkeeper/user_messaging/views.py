from django.shortcuts import render
from accounts.models import CustomUser
from .models import Chat, Message
# Create your views here.

def chat(request,user_id):

	user2 = CustomUser.objects.filter(pk=user_id).first()
	chat = Chat.objects.filter(users=request.user).filter(profiles=user2).distinct().first()

	if chat == None:
		chat = Chat()
		chat.save()
		chat.profiles.add(request.user, user2)
	if request.method == 'POST':
		message = Message(chat=chat, content=request.POST.get('content'), sender=request.user)
		message.save()
	return render(request, 'private_chat.html', {'chat' : chat, 'user2' : user2})

def chat_by_id(request,privatechat_id):
	chat = Chat.objects.filter(pk=privatechat_id).first()
	user2 = chat.profiles.exclude(user=request.user).first()
	return redirect('private_chat', user2.id )

def inbox(request):
	chats = Chat.objects.filter(users=request.user)
	return render(request, 'inbox.html', {'chats' : chats})