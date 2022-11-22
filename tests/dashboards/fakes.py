from django.contrib.auth.models import User

from model_bakery import baker


def fake_user(**kwargs):
    password = kwargs.pop("password", "password")
    user = baker.make(User, **kwargs)
    if isinstance(user, list):
        for u in user:
            u.set_password(password)
            u.save()
    else:
        user.set_password(password)
        user.save()
    return user
