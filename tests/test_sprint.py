import pytest
from rest_framework.test import APIClient

from tests.fixtures import (  # noqa: F401
    admin_client,
    project_1,
    sprint_1,
    user,
    user_client,
)
from tracker.models import Project, Sprint, SprintStatusChoices


@pytest.mark.django_db
class TestGetSprints:
    def test_ok(self, admin_client: APIClient, sprint_1: Sprint):  # noqa: F811
        # Create a sprint for the project
        response = admin_client.get("/api/sprints/")
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]["name"] == sprint_1.name
        assert response.data[0]["status"] == sprint_1.status

    def test_fail_unauthenticated(self):
        client = APIClient()
        response = client.get("/api/sprints/")
        assert response.status_code == 401

    def test_fail_non_admin_user(self, user_client: APIClient):  # noqa: F811
        response = user_client.get("/api/sprints/")
        assert response.status_code == 200


@pytest.mark.django_db
class TestGetSprintDetail:
    def test_ok(self, admin_client: APIClient, sprint_1: Sprint):  # noqa: F811
        response = admin_client.get(f"/api/sprints/{sprint_1.id}/")
        assert response.status_code == 200
        assert response.data["name"] == sprint_1.name
        assert response.data["status"] == sprint_1.status

    def test_fail_nonexistent_sprint(self, admin_client: APIClient):  # noqa: F811
        response = admin_client.get("/api/sprints/999/")
        assert response.status_code == 404

    def test_fail_sprint_unauthenticated(self, sprint_1: Sprint):  # noqa: F811
        client = APIClient()
        response = client.get(f"/api/sprints/{sprint_1.id}/")
        assert response.status_code == 401

    def test_fail_sprint_non_admin_user(
        self,
        user_client: APIClient,  # noqa: F811
        sprint_1: Sprint,  # noqa: F811
    ):
        response = user_client.get(f"/api/sprints/{sprint_1.id}/")
        assert response.status_code == 200


@pytest.mark.django_db
class TestCreateSprint:
    def test_ok(self, admin_client: APIClient, project_1: Project):  # noqa: F811
        data = {
            "project": project_1.id,
            "name": "New Sprint",
            "start_date": "2023-02-01",
            "end_date": "2023-02-15",
        }
        response = admin_client.post("/api/sprints/", data)
        assert response.status_code == 201
        assert response.data["name"] == data["name"]
        assert response.data["status"] == SprintStatusChoices.PLANNED
        assert response.data["project"] == project_1.id

    def test_fail_unauthenticated(self, project_1: Project):  # noqa: F811
        client = APIClient()
        data = {
            "project": project_1.id,
            "name": "New Sprint",
            "start_date": "2023-02-01",
            "end_date": "2023-02-15",
        }
        response = client.post("/api/sprints/", data)
        assert response.status_code == 401

    def test_fail_non_admin_user(
        self,
        user_client: APIClient,  # noqa: F811
        project_1: Project,  # noqa: F811
    ):  # noqa: F811
        data = {
            "project": project_1.id,
            "name": "New Sprint",
            "start_date": "2023-02-01",
            "end_date": "2023-02-15",
        }
        response = user_client.post("/api/sprints/", data)
        assert response.status_code == 403

    def test_fail_invalid_data(
        self,
        admin_client: APIClient,  # noqa: F811
        project_1: Project,  # noqa: F811
    ):
        data = {
            "project": project_1.id,
            "name": "",  # Name is required
            "start_date": "2023-02-01",
            "end_date": "2023-02-15",
        }
        response = admin_client.post("/api/sprints/", data)
        assert response.status_code == 400


@pytest.mark.django_db
class TestUpdateSprint:
    def test_ok(self, admin_client: APIClient, sprint_1: Sprint):  # noqa: F811
        data = {
            "name": "Updated Sprint",
            "start_date": "2023-01-05",
            "end_date": "2023-01-20",
            "status": SprintStatusChoices.ACTIVE,
        }
        response = admin_client.patch(f"/api/sprints/{sprint_1.id}/", data)
        assert response.status_code == 200
        sprint_1.refresh_from_db()
        assert sprint_1.name == data["name"]
        assert sprint_1.start_date.strftime("%Y-%m-%d") == data["start_date"]
        assert sprint_1.end_date.strftime("%Y-%m-%d") == data["end_date"]
        assert sprint_1.status == data["status"]

    def test_fail_unauthenticated(self, sprint_1: Sprint):  # noqa: F811
        client = APIClient()
        data = {
            "name": "Updated Sprint",
            "start_date": "2023-01-05",
            "end_date": "2023-01-20",
            "status": SprintStatusChoices.ACTIVE,
        }
        response = client.patch(f"/api/sprints/{sprint_1.id}/", data)
        assert response.status_code == 401

    def test_fail_non_admin_user(
        self,
        user_client: APIClient,  # noqa: F811
        sprint_1: Sprint,  # noqa: F811
    ):
        data = {
            "name": "Updated Sprint",
            "start_date": "2023-01-05",
            "end_date": "2023-01-20",
            "status": SprintStatusChoices.ACTIVE,
        }
        response = user_client.patch(f"/api/sprints/{sprint_1.id}/", data)
        assert response.status_code == 403

    def test_fail_invalid_data(
        self,
        admin_client: APIClient,  # noqa: F811
        sprint_1: Sprint,  # noqa: F811
    ):
        data = {
            "name": "",  # Name is required
            "start_date": "2023-01-05",
            "end_date": "2023-01-20",
            "status": SprintStatusChoices.ACTIVE,
        }
        response = admin_client.patch(f"/api/sprints/{sprint_1.id}/", data)
        assert response.status_code == 400
        assert "name" in response.data
