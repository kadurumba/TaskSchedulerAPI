from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework import filters, status, generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from scheduler.models import Task
from scheduler.serializers import RegisterSerializer, UserSerializer, TaskSerializer
from django.utils import timezone
from rest_framework.exceptions import PermissionDenied


class CreateUserView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


# User Login View
class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer = UserSerializer

    def post(self, request, *args, **kwargs):
        username = request.data['username']
        password = request.data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            access_token = AccessToken.for_user(user)

            user_data = UserSerializer(user).data

            return Response({
                'access': str(access_token), 'user': user_data
                             })
        else:
            return Response({"error": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)


# User Logout View
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        logout(request)
        return Response({"message": "Successfully logged out"}, status=status.HTTP_200_OK)


class TaskCreateView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Creates new task
    def perform_create(self, serializer):
        instance = serializer.save(user=self.request.user)
        if instance.scheduled_time <= timezone.now():
            instance.status = 'completed'
            instance.save()


class CompletedTaskListView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['status', 'title', 'description', 'user']
    ordering_fields = ['scheduled_time', 'created_at']

    def get_queryset(self):
        user = self.request.user
        status = self.request.query_params.get('status', None)

        if not status or status == "completed":
            tasks = Task.objects.filter(user=user, status="completed")
        else:
            tasks = Task.objects.filter(user=user, status=status)

        for task in tasks:
            if task.scheduled_time <= timezone.now() and task.status != "completed":
                task.status = "completed"
                task.save()

        return tasks


class PendingTaskListView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['status', 'title', 'description', 'user']
    ordering_fields = ['scheduled_time', 'created_at']

    def get_queryset(self):
        user = self.request.user
        status = self.request.query_params.get('status', None)

        if not status or status == "pending":
            tasks = Task.objects.filter(user=user, status="pending")
        else:
            tasks = Task.objects.filter(user=user, status=status)

        for task in tasks:
            if task.scheduled_time > timezone.now() and task.status != "pending":
                task.status = "pending"
                task.save()

        return tasks


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['status', 'title', 'description', 'user']
    ordering_fields = ['scheduled_time', 'created_at']

    """VIEW TO RETRIEVE, UPDATE OR DELETE A TASK"""
    def get_object(self):
        """Ensure that only the task owner can update"""
        task = super().get_object()
        if task.user != self.request.user:
            raise PermissionDenied("You do not have permission to access this task.")
        return task

    def perform_update(self, serializer):
        """"Automatically update status when editing based on some business rules
        This also set time status to completed if scheduled time is in the past"""
        task = serializer.save()
        if task.scheduled_time <= timezone.now() and task.status != 'completed':
            task.status = 'completed'
            task.save()
        elif task.scheduled_time > timezone.now() and task.status != 'pending':
            task.status = 'pending'
            task.save()

    def perform_destroy(self, instance):
        """You can add functionality rule to delete if necessary"""
        instance.delete()
