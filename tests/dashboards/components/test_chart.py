from django.contrib.auth.models import User

import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import pytest

from dashboards.component.chart.serializers import ChartSerializer
from tests.dashboards.fakes import fake_user


pytest_plugins = [
    "tests.dashboards.fixtures",
]


@pytest.fixture()
def test_user_serializer__qs():
    class TestChartSerializer(ChartSerializer):
        class Meta:
            fields = ["id", "username"]
            title = "Users"

        def get_queryset(self, *args, **kwargs):
            return User.objects.all()

        def to_fig(self, df) -> go.Figure:
            fig = px.histogram(
                df,
                x="username",
                y="id",
            )

            return fig

    return TestChartSerializer


@pytest.fixture()
def test_user_serializer__model():
    class TestChartSerializer(ChartSerializer):
        class Meta:
            fields = ["id", "username"]
            model = User
            title = "Users from Model"

        def to_fig(self, df) -> go.Figure:
            fig = px.histogram(
                df,
                x="username",
                y="id",
            )

            return fig

    return TestChartSerializer


@pytest.mark.django_db
def test_serializer__get_data(test_user_serializer__qs):
    for u in range(10, 14):
        fake_user(id=u, username=f"u{u}")

    df = test_user_serializer__qs().get_data()

    assert len(df.index) == User.objects.count()
    assert list(df.columns) == ["id", "username"]


def test_serializer__get_fields(test_user_serializer__qs, snapshot):
    fields = test_user_serializer__qs().get_fields()
    assert fields == ["id", "username"]


def test_serializer__to_fig(snapshot):
    class TestChartSerializer(ChartSerializer):
        def to_fig(self, df) -> go.Figure:
            fig = px.bar(
                df,
                x="col1",
                y="col2",
            )

            return fig

    data = {"col1": [420, 380, 390], "col2": [50, 40, 45]}
    df = pd.DataFrame(data)
    fig = TestChartSerializer().to_fig(df)

    assert isinstance(fig, go.Figure)
    snapshot.assert_match(fig)


def test_serializer__convert_to_df(test_user_serializer__qs):
    data = {"col1": [420, 380, 390], "col2": [50, 40, 45]}
    df = test_user_serializer__qs().convert_to_df(data, columns=["col1", "col2"])

    assert isinstance(df, pd.DataFrame)
    assert len(df.index) == 3
    assert list(df.columns) == ["col1", "col2"]


@pytest.mark.django_db
def test_serializer__serialize__queryset(test_user_serializer__qs, snapshot):
    for u in range(10, 14):
        fake_user(id=u, username=f"u{u}")

    data = test_user_serializer__qs.serialize()

    snapshot.assert_match(data)


@pytest.mark.django_db
def test_serializer__serialize__model(test_user_serializer__model, snapshot):
    for u in range(10, 14):
        fake_user(id=u, username=f"u{u}")

    data = test_user_serializer__model.serialize()

    snapshot.assert_match(data)
