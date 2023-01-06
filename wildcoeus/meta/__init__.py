from typing import Any

from django.apps import apps


class ClassWithMeta:
    _meta: Any

    class Meta:
        abstract = True
        app_label: str
        name: str
        verbose_name: str

    _meta = Meta

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        class MakeMetaConcrete:
            # class to disable "abstract" unless it is
            # overridden by the current class meta
            abstract = False

        # compile a tuple of all the concrete _meta
        # classes prepending the class to turn off
        # the abstract flag
        base_meta_classes = (
            MakeMetaConcrete,
            *(base._meta for base in cls.__bases__ if hasattr(base, "_meta")),
        )

        # if the current class has a Meta class
        # use it as the first base class
        class_meta = cls.__dict__.get("Meta")
        if class_meta:
            base_meta_classes = (
                class_meta,
                *base_meta_classes,
            )

        # build the new concrete _meta class
        cls._meta = type(f"{cls.__name__}ConcreteMeta", base_meta_classes, {})

        # if the current classes Meta class doesn't have
        # the name set, replace the current name with
        # the class name so its not inherited
        if not hasattr(class_meta, "name"):
            cls._meta.name = cls.__name__

        # if the current classes Meta class doesn't have
        # the verbose name set, use the name
        if not hasattr(class_meta, "verbose_name"):
            cls._meta.verbose_name = cls._meta.name

        #
        # ensure that the app config is updated for the new class
        #

        # Look for an application configuration to attach the model to.
        app_config = apps.get_containing_app_config(cls.__module__)

        meta_app_label = getattr(class_meta, "app_label", None)
        if app_config is None and meta_app_label is None:
            raise RuntimeError(
                "%s.%s doesn't declare an explicit "
                "app_label and isn't in an application in "
                "INSTALLED_APPS." % (cls.__module__, cls.__name__)
            )
        else:
            cls._meta.app_label = app_config.label if app_config else meta_app_label
