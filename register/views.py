from django.shortcuts import render,HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.views import View
from .forms import UserForm, LoginForm


class UserFormView(View):
	form_class = UserForm
	template_name = 'home.html'

	def get(self, request):
		form = self.form_class(None)
		context = {
			'form': form,
		}
		return render(request, self.template_name, context)

	def post(self, request):
		form = self.form_class(request.POST)

		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			f_name = form.cleaned_data['first_name']
			l_name = form.cleaned_data['last_name']
			email = form.cleaned_data['email']
			user = User.objects.create_user(username=username)
			user.set_password(password)
			user.email = email
			user.first_name = f_name
			user.last_name = l_name
			user.save()
			user = authenticate(request, username=username, password=password)
			login(request, user)
			return HttpResponseRedirect('/Profile')
		return HttpResponseRedirect('/Home')


def login_user(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return HttpResponseRedirect('/Profile')
	else:
		form = LoginForm(None)
		return render(request, 'login_form.html', {'form': form})

	return render(request, 'login_fail.html', {})
