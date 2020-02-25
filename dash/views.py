from datetime import timedelta, date
from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.views.generic import View
from django.contrib.auth import logout
from django.db.models import Sum
from django.template.loader import get_template
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Task, Goal, SubTask
from .forms import TaskForm, GoalForm
from .serializers import TaskSerializer
from .utils import render_to_pdf


def name(request):
	f_name = request.user.first_name
	l_name = request.user.last_name
	name = f_name + ' ' + l_name
	return name


def index(request):
	tasks = Task.objects.filter(user=request.user)
	comp, all = 0, 0
	for task in tasks:
		if task.active_expiry <= timezone.now().date():
			task.active = False
			task.save()
		if task.final_expiry <= timezone.now().date():
			task.delete()
		if task.completed == True:
			comp += task.priority
		all += task.priority
	goals = Goal.objects.filter(user=request.user)
	for goal in goals:
		if goal.expiry < timezone.now().date():
			goal.delete()
	tasks = Task.objects.filter(user=request.user, completed=True, active=True).count()
	rem_tasks = Task.objects.filter(user=request.user, completed=False, active=True).count()
	rem_goals = Goal.objects.filter(user=request.user, achieved=False).count()
	if all == 0:
		completion= 0
	else:
		completion = (comp/all)*100
	context = {
		'user': request.user,
		'name': name(request),
		'tasks': tasks,
		'rem_tasks': rem_tasks,
		'rem_goals': rem_goals,
		'completion': completion,
	}
	return render(request, 'dashb.html', context)


def logout_user(request):
	logout(request)
	return HttpResponseRedirect('/Home')


def today(request):
	if request.method == 'POST':
		task_form = TaskForm(request.POST)
		if task_form.is_valid():
			task = task_form.save(commit=False)
			task.user = request.user
			task.time *= 60
			task.rating = 0
			task.save()
			return HttpResponseRedirect('today')
	else:
		tasks = Task.objects.filter(user=request.user,completed=False, active=True)
		completed_tasks = Task.objects.filter(user=request.user,completed=True, active=True)
		task_form = TaskForm(None)
		context = {
			'user': request.user,
			'name': name(request),
			'form': task_form,
			'tasks': tasks,
			'completed': completed_tasks,
		}
		return render(request, 'today.html', context)


def complete_task(request, task_id):
	task = Task.objects.get(user=request.user, pk=task_id)
	task.completed = True
	task.save()
	if task.sub_id is not None:
		subtask = SubTask.objects.get(pk=task.sub_id)
		subtask.status = 'CP'
		subtask.save()
	return HttpResponseRedirect('/Profile/today')


def delete_task(request, task_id):
	task = Task.objects.get(user=request.user, pk=task_id)
	task.delete()
	return HttpResponseRedirect('/Profile/today')


def week(request):
	if request.method == 'POST':
		goal_form = GoalForm(request.POST)
		goal = goal_form.save(commit=False)
		goal.user = request.user
		goal.save()
		return HttpResponseRedirect('/Profile/week')
	else:
		goals = Goal.objects.filter(user=request.user,achieved=False)
		achieved_goals = Goal.objects.filter(user=request.user, achieved=True)
		subtasks = SubTask.objects.filter(user=request.user)
		goal_form = GoalForm(None)
		context = {
			'user': request.user,
			'name': name(request),
			'goals': goals,
			'achieved_goals': achieved_goals,
			'form': goal_form,
			'subtasks': subtasks,
		}
		return render(request, 'week.html', context)


def achieve_goal(request, goal_id):
	goal = Goal.objects.get(user=request.user, pk=goal_id)
	goal.achieved = True
	goal.save()
	return HttpResponseRedirect('/Profile/week')


def delete_goal(request):
	goal = Goal.objects.get(user=request.user, pk=request.POST['id'])
	goal.delete()
	return HttpResponseRedirect('/Profile/week')


def add_subtask(request):
	goal_id = request.POST['goal']
	task = request.POST['task']
	subtask = SubTask(task=task, goal=Goal.objects.get(id=goal_id), user=request.user)
	subtask.save()
	return HttpResponseRedirect('/Profile/week')


def delete_subtask(request, subtask_id):
	subtask = SubTask.objects.get(user=request.user,pk=subtask_id)
	if subtask.status == 'IP':
		task = Task.objects.get(sub_id=subtask_id)
		task.delete()
	subtask.delete()
	return HttpResponseRedirect('/Profile/week')


def append_subtask(request):
	subtask = SubTask.objects.get(id=request.POST['subtask'])
	subtask.status = 'IP'
	subtask.save()
	task = Task()
	task.task = subtask.task
	task.sub_id = subtask.id
	min = int(request.POST['time'])
	task.time = timedelta(minutes=min)
	task.category = request.POST['category']
	task.priority = request.POST['priority']
	task.user = request.user
	task.save()
	return HttpResponseRedirect('/Profile/week')


def categories(request):
	context = {
		'user': request.user,
		'name':name(request)
	}
	return render(request,'categories.html',context)


class CategoryChartData(APIView):
	serializer_class = TaskSerializer
	authentication_classes = (SessionAuthentication, BasicAuthentication)
	permission_classes = (IsAuthenticated,)


	def get(self, request, format=None):
		total = Task.objects.filter(user=request.user, completed=True).aggregate(Sum('time'))['time__sum']
		if total is None:
			total = timedelta(seconds=1)
		labels = ['Work', 'Study', 'Sports & Fitness', 'Social',
				  'Fun', 'Errands', 'Self Development', 'Sleep', 'Procrastination']

		categories = ['work', 'study', 'sports', 'social',
				  'fun', 'errands', 'self_dev', 'sleep', 'proc']

		data_set = []
		percentage = []

		for label in categories:
			type = Task.objects.filter(user=request.user, completed=True,
									   category=label).aggregate(Sum('time'))
			if type['time__sum'] is None:
				type['time__sum'] = timedelta(seconds=0)
			today = Task.objects.filter(user=request.user, category=label, completed=True,
										date=date.today()).aggregate(Sum('time'))
			if today['time__sum'] is None:
				today['time__sum'] = timedelta(seconds=0)
			data_set.append(today['time__sum']/60)
			percentage.append(type['time__sum']/total*100)

		data = {
			"labels": labels,
			"data_set": data_set,
			"percentage": percentage,
		}
		return Response(data)


class CompletionChartData(APIView):
	serializer_class = TaskSerializer
	authentication_classes = (SessionAuthentication, BasicAuthentication)
	permission_classes = (IsAuthenticated,)

	def get(self, request, format=None):
		labels = []
		data_set = []
		for x in range(7):
			comp = 0
			all = 0
			labels.append(date.today() - timedelta(days=x))
			tasks = Task.objects.filter(user=request.user, date=labels[x])
			for task in tasks:
				if task.completed == True:
					comp += task.priority
				all += task.priority
			if all == 0:
				val = 0
				data_set.append(val)
			else:
				val = (comp / all) * 100
				data_set.append(val)
		labels.reverse()
		data_set.reverse()
		data = {
			"labels": labels,
			"data_set": data_set,
		}
		return Response(data)


def completion(request):
	dates = []
	for x in range(7):
		dates.append(date.today() - timedelta(days=x))
	context = {
		'user': request.user,
		'name': name(request),
		'dates': dates,
	}
	return render(request, 'completion.html', context)


def reports(request):
	dates = []
	for x in range(7):
		dates.append(date.today() - timedelta(days=x))
	context = {
		'user': request.user,
		'name': name(request),
		'dates': dates,
	}
	return render(request, 'reports.html', context)


class GenerateReportPDF(View):
	def get(self, request, counter):
		val = counter - 1
		day = date.today() - timedelta(days=val)
		comp_tasks = Task.objects.filter(user=request.user, date=day, completed=True)
		rem_tasks = Task.objects.filter(user=request.user, date=day, completed=False)
		context = {
			"name": name(request),
			"completed": comp_tasks,
			"remaining": rem_tasks,
			"date": day,
		}
		pdf = render_to_pdf('report_pdf.html', context)
		if pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			filename = "report.pdf"
			content = "inline; filename=%s" %(filename)
			response['Content-Disposition'] = content
			return response
		return HttpResponse('Not Found')
