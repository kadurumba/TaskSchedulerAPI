from django.contrib import admin
from .models import Task


# Register your models here.
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('username', 'email')
#     list_filter = ('username',)
#     search_fields = ('username', 'email')
#     ordering = ('username', 'email')
#     filter_horizontal = ()


class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'scheduled_time', 'created_at', 'updated_at')
    list_filter = ['status', 'scheduled_time']
    search_fields = ('title', 'description')
    ordering = ['-scheduled_time']


admin.site.register(Task, TaskAdmin)
