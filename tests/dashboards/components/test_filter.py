from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.test import TestCase

from dashboards.component.filters import GenericFilter


class GenericFilterTestCase(TestCase):
    def test_generic_filter(self):
        # Create some test data (adjust as needed)
        user_data = [
            {
                "username": "user1",
                "email": "user1@example.com",
                "age": 25,
                "country": "europe",
            },
            {
                "username": "user2",
                "email": "user2@example.com",
                "age": 30,
                "country": "asia",
            },
            # Add more test data based on your structure
        ]

        # Set the fields you want to filter on
        fields = {
            "username": "char",
            "country": "choice",
        }  # Update with actual field types

        # Create an instance of the GenericFilter
        filter_instance = GenericFilter(
            data=user_data, fields=fields, queryset=User.objects.all()
        )

        # Check if the filter is valid
        self.assertTrue(filter_instance.is_valid())

        # Get the filtered queryset
        filtered_queryset: QuerySet = filter_instance.qs

        # Assert your test cases based on the expected results
        # Check if the queryset is not empty
        self.assertGreater(filtered_queryset.count(), 0)

        # Compare primary keys (IDs) instead of usernames
        user_ids = [user.id for user in filtered_queryset]
        self.assertIn(User.objects.get(username=user_data[0]["username"]).id, user_ids)
        self.assertIn(User.objects.get(username=user_data[1]["username"]).id, user_ids)

        # Add more assertions based on your requirements
