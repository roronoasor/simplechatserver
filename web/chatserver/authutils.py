
from django_mongoengine.mongo_auth.models import User
from django.shortcuts import  redirect

def authenticate(request):
    username = request.POST['username']
    password = request.POST['password']
    try:
        u = User.objects(username=username)
        if password == u[0].password:
            u.is_authenticated = True
            request.user = u
            request.session['is_login'] = True
            request.session['username'] = u[0].username
            print(request.session['username'])
            return u
    except:
        return False
    return False

def create_user(postdata):
    user = User()
    user.username = postdata['username']
    user.email = postdata['email']
    user.password = postdata['password1']
    user.save()
    return user

def login_required(func):
    def inner(request, *args, **kwargs):
        # Get the session to determine whether the user is logged in
        if request.session.get('is_login'):
            print("# Already logged in user...")
            return func(request, *args, **kwargs)
        else:
            return redirect('/chat/login?next='+request.path)
    return inner
