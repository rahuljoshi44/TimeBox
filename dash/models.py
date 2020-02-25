from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta


def set_active_expiry():
	return timezone.now() + timedelta(days=1)


def set_final_expiry():
	return timezone.now() + timedelta(days=7)


class Task(models.Model):
	task = models.CharField(max_length=200)
	time = models.DurationField()
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	date = models.DateField(default=timezone.now)
	active_expiry = models.DateField(default=set_active_expiry)
	final_expiry = models.DateField(default=set_final_expiry)
	PRIORITY_CHOICES = [
		(3, 'High'),
		(2, 'Medium'),
		(1, 'Low'),
	]
	priority = models.IntegerField(choices=PRIORITY_CHOICES)
	CATEGORY_CHOICES = [
		('work', 'Work'),
		('study', 'Study'),
		('sports', 'Sports & Fitness'),
		('social', 'Social'),
		('fun', 'Fun'),
		('errands', 'Errands'),
		('self_dev', 'Self Development'),
		('sleep', 'Sleep/Rest'),
		('proc', 'Procrastination'),
	]
	category = models.CharField(choices=CATEGORY_CHOICES, max_length=30)
	active = models.BooleanField(default=True)
	completed = models.BooleanField(default=False)
	sub_id = models.IntegerField(blank=True, null=True)

	def __str__(self):
		return self.task


class Goal(models.Model):
	title = models.CharField(max_length=200)
	description = models.TextField()
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	achieved = models.BooleanField(default=False)
	date = models.DateField(default=timezone.now)
	expiry = models.DateField(default=set_final_expiry)


class SubTask(models.Model):
	task = models.CharField(max_length=200)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	goal = models.ForeignKey('Goal', on_delete=models.CASCADE)
	status = models.CharField(max_length=100, default='PN')
# Pending, In Progress, Completed  PN  IP  CP
