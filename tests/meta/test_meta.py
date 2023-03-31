from dashboards.meta import ClassWithMeta


class BaseConcreteClass(ClassWithMeta):
    class Meta:
        abstract = True
        default_property = "FOO"
        other_property = "BAR"
        app_label = "metatest"


class SecondBaseConcreteClass(BaseConcreteClass):
    class Meta:
        abstract = True
        default_property_from_second_base = "SECOND FOO"
        other_property_from_second_base = "SECOND BAR"
        app_label = "metatest"


class FirstConcreteClass(BaseConcreteClass):
    class Meta:
        other_property = "BAZ"
        name = "First"
        verbose_name = "First Concrete Class"
        app_label = "metatest"


class SecondConcreteClass(SecondBaseConcreteClass):
    class Meta:
        other_property = "BIFF"
        other_property_from_second_base = "SECOND BIFF"
        name = "Second"
        app_label = "metatest"


def test_base_class():
    assert BaseConcreteClass._meta.abstract is True
    assert BaseConcreteClass._meta.default_property == "FOO"
    assert BaseConcreteClass._meta.other_property == "BAR"
    assert BaseConcreteClass._meta.name == "BaseConcreteClass"
    assert BaseConcreteClass._meta.verbose_name == "BaseConcreteClass"


def test_second_level_base_class():
    assert SecondBaseConcreteClass._meta.abstract is True
    assert BaseConcreteClass._meta.default_property == "FOO"
    assert BaseConcreteClass._meta.other_property == "BAR"
    assert (
        SecondBaseConcreteClass._meta.default_property_from_second_base == "SECOND FOO"
    )
    assert SecondBaseConcreteClass._meta.other_property_from_second_base == "SECOND BAR"
    assert SecondBaseConcreteClass._meta.name == "SecondBaseConcreteClass"
    assert SecondBaseConcreteClass._meta.verbose_name == "SecondBaseConcreteClass"


def test_first_level_concrete_class():
    assert FirstConcreteClass._meta.abstract is False
    assert FirstConcreteClass._meta.default_property == "FOO"
    assert FirstConcreteClass._meta.other_property == "BAZ"
    assert FirstConcreteClass._meta.name == "First"
    assert FirstConcreteClass._meta.verbose_name == "First Concrete Class"


def test_second_level_concrete_class():
    assert SecondConcreteClass._meta.abstract is False
    assert SecondConcreteClass._meta.default_property == "FOO"
    assert SecondConcreteClass._meta.other_property == "BIFF"
    assert SecondConcreteClass._meta.default_property_from_second_base == "SECOND FOO"
    assert SecondConcreteClass._meta.other_property_from_second_base == "SECOND BIFF"
    assert SecondConcreteClass._meta.name == "Second"
    assert SecondConcreteClass._meta.verbose_name == "Second"
