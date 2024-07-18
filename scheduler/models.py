from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta




# Create your models here.
class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed')
    ]

    title = models.CharField(max_length=300)
    description = models.TextField(blank=True, null=True)
    scheduled_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return self.title

    def is_pending(self):
        return self.scheduled_time > timezone.now() and self.status == 'pending'

    def is_completed(self):
        return self.scheduled_time < timezone.now() and self.status == 'completed'


class RecurringTask(models.Model):
    INTERVAL_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]

    task = models.OneToOneField(Task, on_delete=models.CASCADE)
    interval = models.CharField(max_length=10, choices=INTERVAL_CHOICES)
    last_occurrence = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Recurring: {self.task.title}"

    def schedule_next(self):
        now = timezone.now()
        if not self.last_occurrence or self.last_occurrence < now:
            if self.interval == 'daily':
                next_occurrence = self.last_occurrence + timedelta(days=1) if self.last_occurrence else now
            elif self.interval == 'weekly':
                next_occurrence = self.last_occurrence + timedelta(weeks=1) if self.last_occurrence else now
            elif self.interval == 'monthly':
                next_occurrence = self.last_occurrence + timedelta(days=30) if self.last_occurrence else now
            elif self.interval == 'yearly':
                next_occurrence = self.last_occurrence + timedelta(days=365) if self.last_occurrence else now

            new_task = Task.objects.create(
                title=self.task.title,
                description=self.task.description,
                scheduled_time=next_occurrence,
                status='pending'
            )
            self.last_occurrence = next_occurrence
            self.save()
            return new_task
        return None