from typing import Any, Dict

from django.contrib.contenttypes.models import ContentType


def get_object(serializable_object: Dict[str, Any]):
    if not serializable_object:
        return None

    if all(
        key in serializable_object.keys() for key in ["pk", "app_label", "model_name"]
    ):
        return get_django_object(serializable_object)
    else:
        return serializable_object


def get_django_object(serializable_object: Dict[str, Any]):
    object_type = ContentType.objects.get(
        model=serializable_object.get("model_name"),
        app_label=serializable_object.get("app_label"),
    )
    return object_type.get_object_for_this_type(pk=serializable_object.get("pk"))
