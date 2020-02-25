from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm


class UserForm(ModelForm):

	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'username', 'password', 'email']
		widgets = {
			'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'First Name'}),
			'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Last Name'}),
			'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder':' Username'}),
			'password': forms.TextInput(attrs={'class': 'form-control', 'type': 'password', 'placeholder':'Password'}),
			'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Email'}),
		}


class LoginForm(forms.Form):
	username = forms.CharField(max_length=100)
	password = forms.CharField(widget=forms.PasswordInput)
	username.widget.attrs.update({'class': 'form-control', 'placeholder':'Username'})
	password.widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})


