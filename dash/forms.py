from django.forms import ModelForm
from .models import Task, Goal
from django import forms

class TaskForm(ModelForm):
	class Meta:
		model = Task
		fields = ['task', 'time', 'priority', 'category']


class GoalForm(ModelForm):
	class Meta:
		model = Goal
		fields = ['title', 'description']
		widgets = {
			'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
			'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
		}
