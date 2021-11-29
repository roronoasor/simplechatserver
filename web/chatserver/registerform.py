from django import forms
from django_mongoengine.mongo_auth.models import User



class NewUserForm(forms.Form):
	username = forms.CharField(label='Your username', max_length=50)
	email = forms.EmailField(label='Your email', max_length=50)
	password1 = forms.CharField(label='Your Password', max_length=50, widget=forms.PasswordInput())
	password2 = forms.CharField(label='Repeat Password again', max_length=50, widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")
