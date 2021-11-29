from django.shortcuts import render

from django.shortcuts import  render, redirect
from .registerform import NewUserForm
from .loginform import LoginForm
from django.contrib import messages

from .models import User, Chatroom
# from django_mongoengine.mongo_auth.models import User

from .authutils import create_user, authenticate, login_required

# view for creating a new chat room
@login_required
def index(request):
	return render(request, 'chatserver/newroom.html')

# view for Chat room
@login_required
def room(request, room_name):
	return render(request, 'chatserver/chatroom.html', {
		'room_name': room_name,
		'loggedinusername': request.session['username']
	})

# view for Chat room Information
@login_required
def chatinfo(request, room_name):
	chatroom = Chatroom.objects(chatroom="chat_" + room_name)
	return render(request, 'chatserver/chatroominfo.html', {
		'room_name': room_name,
		'userlist': chatroom[0].users
	})

# view for Registering new users
def register_request(request):

	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			u = create_user(request.POST)
			u.is_authenticated = True
			request.session['is_login'] = True
			request.session['username'] = u.username
			messages.success(request, "Registration successful." )
			return redirect("/chat")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="chatserver/register.html", context={"register_form":form})

# view for logging in users
def login(request):
	redirect_to = request.GET.get("next", None)
	if request.method == "POST":
		form = LoginForm(request.POST)
		if form.is_valid():
			user = authenticate(request)
			if user is not False:
				messages.success(request, "Login successful." )
				return redirect(redirect_to)
			else:
				messages.error(request, "Unsuccessful Login. Invalid information.")
		messages.error(request, "Unsuccessful Login. Invalid information.")
	form = LoginForm()
	return render(request=request, template_name="chatserver/login.html", context={"login_form":form})