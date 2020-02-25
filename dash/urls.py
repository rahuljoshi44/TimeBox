from django.urls import path
from . import views


urlpatterns = [
	# Dashboard
	path('', views.index),
	path('Dashboard', views.index),
	path('logout', views.logout_user),
	# Today
	path('today', views.today),
	path('today/complete/<int:task_id>', views.complete_task),
	path('today/delete/<int:task_id>', views.delete_task),
	# Week
	path('week', views.week), # Add Goal
	path('week/achieve/<int:goal_id>', views.achieve_goal), # Finish Goal
	path('week/delete/goal', views.delete_goal), # Delete Goal
	path('week/task/delete/<int:subtask_id>', views.delete_subtask), # Delete sub-task
	path('week/task/append', views.append_subtask), # Append sub-task
	path('week/add/subtask', views.add_subtask), # Add Subtask
	# Category
	path('categories', views.categories),
	path('api/category-data', views.CategoryChartData.as_view()),
	# Completion
	path('completion', views.completion),
	path('api/productivity-data', views.CompletionChartData.as_view()),
	# Reports
	path('reports', views.reports),
	path('reports/pdf/<int:counter>', views.GenerateReportPDF.as_view())
]
