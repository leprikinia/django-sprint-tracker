from django.urls import path, include
from rest_framework.routers import DefaultRouter
from tracker.viewsets import ProjectViewSet, SprintViewSet, TaskViewSet

router = DefaultRouter()
router.register(r'sprints', SprintViewSet)
router.register(r'tasks', TaskViewSet)
router.register(r'projects', ProjectViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
