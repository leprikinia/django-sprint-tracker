from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from tracker.models import Project, Sprint, Task
from tracker.permissions import IsAdminOrReadOnly, IsAssigneeOrAdmin
from tracker.serializers import ProjectSerializer, SprintSerializer, TaskSerializer

User = get_user_model()


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated & IsAdminOrReadOnly]


class SprintViewSet(ModelViewSet):
    queryset = Sprint.objects.all()
    serializer_class = SprintSerializer
    permission_classes = [IsAuthenticated & IsAdminOrReadOnly]


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.select_related("sprint", "assignee").all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated & IsAssigneeOrAdmin]

    @action(detail=True, methods=["patch"])
    def assign(self, request, pk: int):
        user_id = request.data.get("user")
        task = self.get_object()

        if not user_id:
            return Response({"error": "user is required"}, status=400)

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        task.assignee = user
        task.save()
        return Response(status=200)
