from typing import Any, Dict

from django.contrib.contenttypes.models import ContentType


def get_object(serializable_object: Dict[str, Any]):
    """
    Converts a serialized object into a concrete python object.
    This will either return the original ``serializable_object``
    or django model object if the ``serializable_object`` has
    the following keys:

    * ``pk``: The id of the object in the database
    * ``app_label``: The name of the django app the object belongs to
    * ``model_name``: The name of the objects model

    :param serializable_object: The json object to convert
    """
    if not serializable_object:
        return None

    if all(
        key in serializable_object.keys() for key in ["pk", "app_label", "model_name"]
    ):
        return get_django_object(serializable_object)
    else:
        return serializable_object


def get_django_object(serializable_object: Dict[str, Any]):
    """
    Converts a serialized object into a django ORM object.
    The ``serializable_object`` must have the following keys:

    * ``pk``: The id of the object in the database
    * ``app_label``: The name of the django app the object belongs to
    * ``model_name``: The name of the objects model

    :param serializable_object: The json object to convert
    """

    object_type = ContentType.objects.get(
        model=serializable_object.get("model_name"),
        app_label=serializable_object.get("app_label"),
    )
    return object_type.get_object_for_this_type(pk=serializable_object.get("pk"))
