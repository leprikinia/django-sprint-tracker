import pytest
from rest_framework.test import APIClient

from tests.fixtures import admin_client, project_1, user, user_client  # noqa: F401
from tracker.models import Project


@pytest.mark.django_db
class TestGetProjects:
    def test_get_projects(self, admin_client: APIClient, project_1: Project):  # noqa: F811
        response = admin_client.get("/api/projects/")
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]["name"] == project_1.name
        assert response.data[0]["description"] == project_1.description

    def test_get_projects_unauthenticated(self):
        client = APIClient()
        response = client.get("/api/projects/")
        assert response.status_code == 401

    def test_get_projects_non_admnin_user(self, user_client: APIClient):  # noqa: F811
        response = user_client.get("/api/projects/")
        assert response.status_code == 200


@pytest.mark.django_db
class TestGetProjectDetail:
    def test_ok(self, admin_client: APIClient, project_1: Project):  # noqa: F811
        response = admin_client.get(f"/api/projects/{project_1.id}/")
        assert response.status_code == 200
        assert response.data["name"] == project_1.name
        assert response.data["description"] == project_1.description

    def test_get_nonexistent_project(self, admin_client: APIClient):  # noqa: F811
        response = admin_client.get("/api/projects/999/")
        assert response.status_code == 404

    def test_get_project_unauthenticated(self, project_1: Project):  # noqa: F811
        client = APIClient()
        response = client.get(f"/api/projects/{project_1.id}/")
        assert response.status_code == 401

    def test_get_projects_non_admnin_user(
        self,
        user_client: APIClient,  # noqa: F811
        project_1: Project,  # noqa: F811
    ):
        response = user_client.get(f"/api/projects/{project_1.id}/")
        assert response.status_code == 200


@pytest.mark.django_db
class TestCreateProject:
    def test_create_project(self, admin_client: APIClient):  # noqa: F811
        data = {
            "name": "New Project",
            "description": "New Description",
        }
        response = admin_client.post("/api/projects/", data)
        assert response.status_code == 201
        assert response.data["name"] == data["name"]
        assert response.data["description"] == data["description"]
        assert Project.objects.filter(name="New Project").exists()

    def test_create_project_unauthenticated(self):
        client = APIClient()
        data = {
            "name": "New Project",
            "description": "New Description",
        }
        response = client.post("/api/projects/", data)
        assert response.status_code == 401

    def test_create_project_non_admin_user(self, user_client: APIClient):  # noqa: F811
        data = {
            "name": "New Project",
            "description": "New Description",
        }
        response = user_client.post("/api/projects/", data)
        assert response.status_code == 403

    def test_create_project_invalid_data(self, admin_client: APIClient):  # noqa: F811
        data = {
            "name": "",  # Name is required
            "description": "New Description",
        }
        response = admin_client.post("/api/projects/", data)
        assert response.status_code == 400
        assert "name" in response.data


@pytest.mark.django_db
class TestUpdateProject:
    def test_update_project(self, admin_client: APIClient, project_1: Project):  # noqa: F811
        data = {
            "name": "Updated Project",
            "description": "Updated Description",
        }
        response = admin_client.put(f"/api/projects/{project_1.id}/", data)
        assert response.status_code == 200
        project_1.refresh_from_db()
        assert project_1.name == data["name"]
        assert project_1.description == data["description"]

    def test_update_project_unauthenticated(self, project_1: Project):  # noqa: F811
        client = APIClient()
        data = {
            "name": "Updated Project",
            "description": "Updated Description",
        }
        response = client.put(f"/api/projects/{project_1.id}/", data)
        assert response.status_code == 401

    def test_update_project_non_admin_user(
        self,
        user_client: APIClient,  # noqa: F811
        project_1: Project,  # noqa: F811
    ):
        data = {
            "name": "Updated Project",
            "description": "Updated Description",
        }
        response = user_client.put(f"/api/projects/{project_1.id}/", data)
        assert response.status_code == 403

    def test_update_project_invalid_data(
        self,
        admin_client: APIClient,  # noqa: F811
        project_1: Project,  # noqa: F811
    ):
        data = {
            "name": "",  # Name is required
            "description": "Updated Description",
        }
        response = admin_client.put(f"/api/projects/{project_1.id}/", data)
        assert response.status_code == 400
        assert "name" in response.data
