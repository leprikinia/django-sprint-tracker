import pytest
from rest_framework.test import APIClient

from tests.fixtures import (  # noqa: F401
    User,
    admin_client,
    project_1,
    sprint_1,
    task_1,
    user,
    user_client,
)
from tracker.models import Project, Sprint, Task, TaskStatusChoices


@pytest.mark.django_db
class TestGetTasks:
    def test_ok(self, admin_client: APIClient, task_1: Task):  # noqa: F811
        # Create a task for the project
        response = admin_client.get("/api/tasks/")
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]["title"] == task_1.title
        assert response.data[0]["status"] == task_1.status

    def test_fail_unauthenticated(self):
        client = APIClient()
        response = client.get("/api/tasks/")
        assert response.status_code == 401

    def test_fail_non_admin_user(self, user_client: APIClient):  # noqa: F811
        response = user_client.get("/api/tasks/")
        assert response.status_code == 200


@pytest.mark.django_db
class TestGetTaskDetail:
    def test_ok(self, admin_client: APIClient, task_1: Task):  # noqa: F811
        response = admin_client.get(f"/api/tasks/{task_1.id}/")
        assert response.status_code == 200
        assert response.data["title"] == task_1.title
        assert response.data["status"] == task_1.status

    def test_fail_nonexistent_task(self, admin_client: APIClient):  # noqa: F811
        response = admin_client.get("/api/tasks/999/")
        assert response.status_code == 404

    def test_fail_task_unauthenticated(self, task_1: Task):  # noqa: F811
        client = APIClient()
        response = client.get(f"/api/tasks/{task_1.id}/")
        assert response.status_code == 401

    def test_fail_task_non_admin_user(
        self,
        user_client: APIClient,  # noqa: F811
        task_1: Task,  # noqa: F811
    ):
        response = user_client.get(f"/api/tasks/{task_1.id}/")
        assert response.status_code == 200


@pytest.mark.django_db
class TestCreateTask:
    def test_ok(
        self,
        admin_client: APIClient,  # noqa: F811
        project_1: Project,  # noqa: F811
        sprint_1: Sprint,  # noqa: F811
    ):  # noqa: F811
        data = {
            "project": project_1.id,
            "sprint": sprint_1.id,
            "title": "New Task",
            "description": "New Task Description",
            "status": TaskStatusChoices.TO_DO,
        }
        response = admin_client.post("/api/tasks/", data)
        assert response.status_code == 201
        assert response.data["title"] == data["title"]
        assert response.data["description"] == data["description"]
        assert response.data["status"] == data["status"]
        assert response.data["project"] == data["project"]
        assert response.data["sprint"] == data["sprint"]

    def test_ok_create_task_no_sprint(
        self,
        admin_client: APIClient,  # noqa: F811
        project_1: Project,  # noqa: F811
    ):  # noqa: F811
        data = {
            "project": project_1.id,
            "title": "New Task without sprint",
            "description": "New Task Description",
            "status": TaskStatusChoices.TO_DO,
        }
        response = admin_client.post("/api/tasks/", data)
        assert response.status_code == 201
        assert response.data["title"] == data["title"]
        assert response.data["description"] == data["description"]
        assert response.data["status"] == data["status"]
        assert response.data["project"] == data["project"]
        assert response.data["sprint"] is None

    def test_fail_unauthenticated(self, project_1: Project, sprint_1: Sprint):  # noqa: F811
        client = APIClient()
        data = {
            "project": project_1.id,
            "sprint": sprint_1.id,
            "title": "New Task",
            "description": "New Task Description",
            "status": TaskStatusChoices.TO_DO,
        }
        response = client.post("/api/tasks/", data)
        assert response.status_code == 401

    def test_fail_non_admin_user(
        self,
        user_client: APIClient,  # noqa: F811
        project_1: Project,  # noqa: F811
        sprint_1: Sprint,  # noqa: F811
    ):  # noqa: F811
        # In current permissions non-admin user can create tasks
        data = {
            "project": project_1.id,
            "sprint": sprint_1.id,
            "title": "New Task",
            "description": "New Task Description",
            "status": TaskStatusChoices.TO_DO,
        }
        response = user_client.post("/api/tasks/", data)
        print(response.data)
        assert response.status_code == 201


@pytest.mark.django_db
class TestUpdateTask:
    def test_ok(
        self,
        admin_client: APIClient,  # noqa: F811
        task_1: Task,  # noqa: F811
    ):
        data = {
            "title": "Updated Task Title",
            "description": "Updated Task Description",
            "status": TaskStatusChoices.IN_PROGRESS,
        }
        response = admin_client.patch(f"/api/tasks/{task_1.id}/", data)
        assert response.status_code == 200
        assert response.data["title"] == data["title"]
        assert response.data["description"] == data["description"]
        assert response.data["status"] == data["status"]

    def test_fail_unauthenticated(self, task_1: Task):  # noqa: F811
        client = APIClient()
        data = {
            "title": "Updated Task Title",
            "description": "Updated Task Description",
            "status": TaskStatusChoices.IN_PROGRESS,
        }
        response = client.patch(f"/api/tasks/{task_1.id}/", data)
        assert response.status_code == 401

    def test_fail_non_admin_user_not_assignee(
        self,
        user_client: APIClient,  # noqa: F811
        task_1: Task,  # noqa: F811
    ):
        data = {
            "title": "Updated Task Title",
            "description": "Updated Task Description",
            "status": TaskStatusChoices.IN_PROGRESS,
        }
        response = user_client.patch(f"/api/tasks/{task_1.id}/", data)
        assert response.status_code == 403

    def test_fail_non_admin_user_assignee(
        self,
        user_client: APIClient,  # noqa: F811
        task_1: Task,  # noqa: F811
        user: User,  # noqa: F811 # type: ignore
    ):
        # Assign the task to the user
        task_1.assignee = user
        task_1.save()
        data = {
            "title": "Updated Task Title by Assignee",
            "description": "Updated Task Description by Assignee",
            "status": TaskStatusChoices.IN_PROGRESS,
        }
        response = user_client.patch(f"/api/tasks/{task_1.id}/", data)
        assert response.status_code == 200
        assert response.data["title"] == data["title"]
        assert response.data["description"] == data["description"]
        assert response.data["status"] == data["status"]
