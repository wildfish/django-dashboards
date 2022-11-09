from django.contrib.auth.models import User

from model_bakery import baker


def fake_user(**kwargs):
    password = kwargs.pop("password", "password")
    user = baker.make(User, **kwargs)
    user.set_password(password)
    user.save()
    return user
