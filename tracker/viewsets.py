from tracker.models import Project, Sprint, Task
from tracker.permissions import IsAdminOrReadOnly, IsAssigneeOrAdmin
from tracker.serializers import ProjectSerializer, SprintSerializer, TaskSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated & IsAdminOrReadOnly]


class SprintViewSet(ModelViewSet):
    queryset = Sprint.objects.all()
    serializer_class = SprintSerializer
    permission_classes = [IsAuthenticated & IsAdminOrReadOnly]


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.select_related('sprint', 'assignee').all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated & IsAssigneeOrAdmin]
