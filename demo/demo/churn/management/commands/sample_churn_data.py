from django.core.management.base import BaseCommand

from model_bakery import baker

from demo.churn.models import Customer


class Command(BaseCommand):
    def handle(self, *args, **options):
        Customer.objects.all().delete()
        for _ in range(500):
            baker.make_recipe("churn.fake_customer")
