from random import randint

from faker import Faker
from model_bakery.recipe import Recipe

from demo.churn.models import Customer


fake = Faker()


def get_bool():
    return randint(0, 1)


fake_customer = Recipe(
    Customer,
    reference=fake.swift,
    name=fake.company,
    phone=fake.phone_number,
    email=fake.ascii_email,
    location=fake["en-US"].state,
    faults=lambda: randint(0, 100),
    sla_breaches=lambda: randint(0, 20),
    ownership_changes=lambda: randint(0, 2),
    product_cloud=get_bool,
    product_connectivity=get_bool,
    product_licenses=get_bool,
    product_managed_services=get_bool,
    product_backup=get_bool,
    product_hardware=get_bool,
    contract_start_date=fake.date_time_this_year,
    contract_end_date=lambda: fake.date_time_this_year()
    if randint(0, 20) > 1
    else None,
    recurring_revenue=lambda: randint(5000, 200000),
    non_recurring_revenue=lambda: randint(500, 10000),
)
