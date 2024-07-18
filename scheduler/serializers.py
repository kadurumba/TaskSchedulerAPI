from rest_framework import serializers
from .models import Task, RecurringTask



class TaskSerializer(serializers.ModelSerializer):


    class Meta:
        model = Task
        fields = ['title', 'description', 'scheduled_time', 'created_at', 'updated_at', 'status', 'is_pending', 'is_completed']
        read_only_fields = ['created_at', 'updated_at', 'is_pending', 'is_completed']


class RecurringTaskSerializer(serializers.ModelSerializer):
    task = TaskSerializer(read_only=True)


    class Meta:
        model =RecurringTask
        fields = ['task', 'interval', 'last_occurrence']
        read_only_fields = ['task', 'last_occurrence']