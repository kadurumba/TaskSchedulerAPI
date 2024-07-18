"""
URL configuration for taskscheduler project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import TaskViewSet, RecurringTaskViewSet, TaskUpdateView, TaskDeleteView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('', TaskViewSet.as_view(), name='Task'),
    path('', RecurringTaskViewSet.as_view(), name='Recuring'),
    path('task/<int:pk>/update', TaskUpdateView.as_view(), name='delete_task'),
    path('task/<int:pk>/delete', TaskDeleteView.as_view(), name='delete_task'),
    path('api/token/', obtain_auth_token, name='obtain'),
]
