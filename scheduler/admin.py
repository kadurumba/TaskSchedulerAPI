from django.contrib import admin
from .models import Task, RecurringTask

# Register your models here.
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'scheduled_time', 'created_at', 'updated_at')
    list_filter = ['status', 'scheduled_time']
    search_fields = ('title', 'description')
    ordering = ['-scheduled_time']

class RecurringTaskAdmin(admin.ModelAdmin):
    list_display = ('task', 'interval', 'last_occurrence')
    list_filter = ['interval']

admin.site.register(Task, TaskAdmin)
admin.site.register(RecurringTask, RecurringTaskAdmin)