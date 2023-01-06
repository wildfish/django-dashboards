from unittest.mock import patch

from django.contrib.auth.models import User

import pytest
import strawberry

from tests.dashboards.app1.dashboards import (
    TestAdminDashboard,
    TestComplexDashboard,
    TestDashboard,
    TestDashboardWithLayout,
    TestDashboardWithMetaName,
    TestDashboardWithMetaVerboseName,
    TestFilterDashboard,
    TestModelDashboard,
    TestNoMetaDashboard,
)
from wildcoeus.dashboards.schema import DashboardQuery


@pytest.fixture(autouse=True)
def mock_random_ms_delay():
    with patch(
        "wildcoeus.dashboards.templatetags.wildcoeus.random.randint"
    ) as random_ms_delay:
        random_ms_delay.return_value = 1
        yield random_ms_delay


@pytest.fixture
def schema():
    return strawberry.Schema(query=DashboardQuery)


@pytest.fixture
def dashboard():
    return TestDashboard


@pytest.fixture
def complex_dashboard():
    return TestComplexDashboard


@pytest.fixture
def admin_dashboard():
    return TestAdminDashboard


@pytest.fixture
def model_dashboard():
    return TestModelDashboard


@pytest.fixture
def filter_dashboard():
    return TestFilterDashboard


@pytest.fixture
def dashboard_with_layout(dashboard):
    return TestDashboardWithLayout


@pytest.fixture
def no_meta_dashboard(dashboard):
    return TestNoMetaDashboard


@pytest.fixture
def named_meta_dashboard(dashboard):
    return TestDashboardWithMetaName


@pytest.fixture
def verbose_named_meta_dashboard(dashboard):
    return TestDashboardWithMetaVerboseName


@pytest.fixture
def user():
    user = User.objects.create(
        username="tester", is_active=True, email="tester@test.com"
    )
    user.set_password("password")
    user.save()
    return user


@pytest.fixture
def staff():
    user = User.objects.create(
        username="tester", is_active=True, email="tester@test.com", is_staff=True
    )
    user.set_password("password")
    user.save()
    return user
