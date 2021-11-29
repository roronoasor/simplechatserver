from django import forms
# from .models import User
from django_mongoengine.mongo_auth.models import User


class LoginForm(forms.Form):
	username = forms.CharField(label='Your username', max_length=50)
	password = forms.CharField(label='Your Password', max_length=50, widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ("username", "password")
