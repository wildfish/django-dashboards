# from django.core.exceptions import PermissionDenied
# from django.http import Http404

from django.urls import reverse

import pytest

from wildcoeus.pipelines.base import pipeline_registry


# from wildcoeus.pipelines.views import PipelineListView


pytest_plugins = [
    "tests.pipelines.fixtures",
]

pytestmark = pytest.mark.django_db


def test_pipeline_list__no_permission(client):
    response = client.get(reverse("wildcoeus.pipelines:list"))

    assert response.status_code == 302


def test_pipeline_list(client, user):
    client.force_login(user)
    response = client.get(reverse("wildcoeus.pipelines:list"))

    assert response.status_code == 200
    assert "pipelines" in list(response.context_data.keys())
    assert len(response.context_data["pipelines"]) == 4
