from django.urls import path
from . import views

urlpatterns = [
	path('', views.UserFormView.as_view()),
	path('login',views.login_user),
]
