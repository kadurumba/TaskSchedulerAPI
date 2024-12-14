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
from .views import CreateUserView, LoginView, LogoutView, TaskCreateView, CompletedTaskListView, PendingTaskListView, TaskDetailView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('register/', CreateUserView.as_view(), name='CreateUser'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('completed_task/', CompletedTaskListView.as_view(), name='completed-task'),
    path('pending_task/', PendingTaskListView.as_view(), name='pending-task'),
    path('create_task/', TaskCreateView.as_view(), name='task-create'),
    path('<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('api/task/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/task/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
