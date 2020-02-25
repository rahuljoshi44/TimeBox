from django.contrib import admin
from .models import Task, Goal, SubTask


class TaskAdmin(admin.ModelAdmin):
	list_display = ('user', 'task', 'time')


class GoalAdmin(admin.ModelAdmin):
	list_display = ('user', 'title')


class SubTaskAdmin(admin.ModelAdmin):
	list_display = ('user', 'task')


admin.site.register(Task, TaskAdmin)
admin.site.register(Goal, GoalAdmin)
admin.site.register(SubTask, SubTaskAdmin)
