import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from tracker.models import Project, Sprint, Task, TaskStatusChoices

User = get_user_model()


@pytest.fixture
def project_1():
    return Project.objects.create(
        name="Project 1",
        description="Description 1",
    )


@pytest.fixture
def sprint_1(project_1: Project):
    return Sprint.objects.create(
        project=project_1,
        name="Sprint 1",
        start_date="2023-01-01",
        end_date="2023-01-15",
    )


@pytest.fixture
def task_1(project_1: Project, sprint_1: Sprint):
    return Task.objects.create(
        project=project_1,
        sprint=sprint_1,
        title="Task 1",
        description="Task Description 1",
        status=TaskStatusChoices.TO_DO,
    )


@pytest.fixture
def admin_user():
    return User.objects.create_user(
        username="test-admin",
        password="tfiPgh-1rtbUi",
        is_staff=True,
    )


@pytest.fixture
def admin_client(admin_user):
    client = APIClient()
    client.force_authenticate(admin_user)
    return client


@pytest.fixture
def user():
    return User.objects.create_user(
        username="test-user",
        password="mAkfol-6yTeqa",
        is_staff=False,
    )


@pytest.fixture
def user_client(user):
    client = APIClient()
    client.force_authenticate(user)
    return client
