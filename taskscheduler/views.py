from rest_framework.views import APIView
from rest_framework import filters, status
from rest_framework.response import Response

from scheduler.models import Task, RecurringTask
from scheduler.serializers import TaskSerializer, RecurringTaskSerializer
from django.shortcuts import get_object_or_404


# Create your views here.
class TaskViewSet(APIView):

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['status', 'title', 'description']
    ordering_fields = ['scheduled_time', 'created_at']

    def post(self, request, *args, **kwargs):
        serializer_class = TaskSerializer(data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data)
        return Response(serializer_class.errors)

    def get(self, request, *args, **kwargs):
        queryset = Task.objects.all()
        serializer_class = TaskSerializer(queryset, many=True)
        return Response(serializer_class.data)

    def pending(self, request, *args, **kwargs):
        queryset = Task.objects.all()
        pending_tasks = queryset.filter(status='pending')
        serializer_class = TaskSerializer(pending_tasks)
        return Response(serializer_class.data)

    def completed(self, request, *args, **kwargs):
        queryset = Task.objects.all()
        completed_tasks = queryset.filter(status='completed')
        serializer_class = TaskSerializer(completed_tasks)
        return Response(serializer_class.data)


class TaskUpdateView(APIView):

    def put(self, request, pk, format=None):
        task_update = get_object_or_404(Task, pk=pk)
        serializer_class = TaskSerializer(task_update, data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data)
        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        # Override partial_update method to handle partial updates via PATCH
        partial_update = get_object_or_404(Task, pk=pk)
        serializer_class = TaskSerializer(partial_update, data=request.data, partial=True)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data)
        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDeleteView(APIView):
    def delete_task(self, request, pk, format=None):
        destroy = get_object_or_404(Task, pk=pk)
        destroy.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RecurringTaskViewSet(APIView):
    queryset = RecurringTask.objects.all()
    serializer_class = RecurringTaskSerializer