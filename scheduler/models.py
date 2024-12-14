from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed')
    ]
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True, null=True)
    scheduled_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='', null=True)

    def __str__(self):
        return self.title

    def is_pending(self):
        return self.status == 'pending' and self.scheduled_time > timezone.now()

    def is_completed(self):
        return self.status == 'completed' and self.scheduled_time <= timezone.now()
