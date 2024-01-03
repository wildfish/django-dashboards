from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.test import TestCase

from dashboards.component.filters import GenericFilter


def test_generic_filter(self):
    self.assertTrue(self.filter_instance.is_valid())

    filtered_queryset: QuerySet = self.filter_instance.qs

    print("User Data:", self.user_data)
    print("Fields:", self.fields)
    print("Filtered Usernames:", [user.username for user in filtered_queryset])

    self.assertGreater(filtered_queryset.count(), 0)

    for user_data in self.user_data:
        username = user_data["username"]
        print(f"Checking if user '{username}' is in filtered queryset.")
        self.assertIn(username, [user.username for user in filtered_queryset])

        if "country" in self.fields:
            country_value = self.fields["country"]
            user = User.objects.get(username=username)
            self.assertEqual(user.country, country_value)
