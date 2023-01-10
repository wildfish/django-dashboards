from typing import Type, Union

from django.apps import apps


class ClassWithMeta:
    _meta: Type["ClassWithMeta.Meta"]

    class Meta:
        abstract = True
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
        class_meta = cls.preprocess_meta(
            type("Meta", (class_meta,), {}) if class_meta else None
        )
        if class_meta:
            base_meta_classes = (
                class_meta,
                *base_meta_classes,
            )

        # build the new concrete _meta class
        _meta = type(f"{cls.__name__}ConcreteMeta", base_meta_classes, {})

        # if the current classes Meta class doesn't have
        # the name set, replace the current name with
        # the class name so its not inherited
        if not hasattr(class_meta, "name"):
            _meta.name = cls.__name__

        # if the current classes Meta class doesn't have
        # the verbose name set, use the name
        if not hasattr(class_meta, "verbose_name"):
            _meta.verbose_name = _meta.name

        # run the postprocess meta hook
        cls._meta = cls.postprocess_meta(class_meta, _meta)

    def __str__(self):
        return self._meta.verbose_name

    @classmethod
    def preprocess_meta(cls, current_class_meta: Union[None, type]):
        """
        Preprocesses the meta class attached to the class being created.

        The current_class_meta class will be a copy of the class attached to
        the class being initialised so can be safely modified.

        current_class_meta: The meta class attached to the current class.
            If no Meta class is set on the current class the value is None.
        """
        return current_class_meta

    @classmethod
    def postprocess_meta(cls, current_class_meta, resolved_meta_class):
        """
        Postprocesses the resolved meta class to be attached to the class
        being created.

        The current_class_meta class will be a copy of the class attached to
        the class being initialised so can be safely modified.

        current_class_meta: The meta class attached to the current class.
            If no Meta class is set on the current class the value is None.
        resolved_meta_class: The resolved meta class created from the current
            class meta and all the meta classes attached to the classes bases
        """
        return resolved_meta_class

    def get_meta(self):
        return self._meta


class ClassWithAppConfigMeta(ClassWithMeta):
    _meta: Type["ClassWithAppConfigMeta.Meta"]

    class Meta(ClassWithMeta.Meta):
        abstract = True
        app_label: str

    @classmethod
    def postprocess_meta(cls, class_meta, resolved_meta_class):
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
            resolved_meta_class.app_label = (
                app_config.label if app_config else meta_app_label
            )

        return super().postprocess_meta(class_meta, resolved_meta_class)
