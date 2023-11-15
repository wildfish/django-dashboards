from dataclasses import dataclass, field
from datetime import timedelta
from typing import Any, Optional, Type

from django.core.exceptions import ImproperlyConfigured
from django.db.models import Aggregate, Model, QuerySet
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.timesince import timesince

import asset_definitions

from dashboards.meta import ClassWithMeta


@dataclass
class StatSerializerData:
    title: str
    value: Any
    previous: Optional[Any] = None
    unit: Optional[str] = ""
    change_period: Optional[str] = ""
    change: Optional[float] = field(init=False)

    def __post_init__(self):
        if self.previous is None:
            self.change = 0.0
        elif self.previous == 0:
            self.change = 100.0
        else:
            try:
                self.change = (self.value - self.previous) / self.previous * 100
            except (TypeError, ZeroDivisionError):
                self.change = None


class BaseStatSerializer(ClassWithMeta):
    class Meta(ClassWithMeta.Meta):
        annotation_field: str
        annotation: Aggregate
        model: Optional[Model] = None
        title: Optional[str] = ""
        unit: Optional[str] = ""

    _meta: Type["BaseStatSerializer.Meta"]

    @classmethod
    def preprocess_meta(cls, current_class_meta):
        title = getattr(current_class_meta, "title", None)

        if title and not hasattr(current_class_meta, "name"):
            current_class_meta.name = title

        if title and not hasattr(current_class_meta, "verbose_name"):
            current_class_meta.verbose_name = title

        return current_class_meta

    @classmethod
    def postprocess_meta(cls, current_class_meta, resolved_meta_class):
        if not hasattr(resolved_meta_class, "title"):
            resolved_meta_class.title = resolved_meta_class.verbose_name

        return resolved_meta_class

    @property
    def annotated_field_name(self) -> str:
        return f"{self._meta.annotation.name.lower()}_{self._meta.annotation_field}"

    def aggregate_queryset(self, queryset) -> QuerySet:
        # apply aggregation to queryset to get single value
        queryset = queryset.aggregate(
            **{
                self.annotated_field_name: self._meta.annotation(
                    self._meta.annotation_field
                )
            }
        )

        return queryset

    def get_queryset(self, *args, **kwargs) -> QuerySet:
        if self._meta.model is not None:
            queryset = self._meta.model._default_manager.all()
        else:
            raise ImproperlyConfigured(
                "%(self)s is missing a QuerySet. Define "
                "%(self)s.model or override "
                "%(self)s.get_queryset()." % {"self": self.__class__.__name__}
            )

        return queryset

    @classmethod
    def serialize(cls, **kwargs) -> StatSerializerData:
        raise NotImplementedError


class StatSerializer(BaseStatSerializer, asset_definitions.MediaDefiningClass):
    template_name: str = "dashboards/components/stat/stat.html"

    class Media:
        js = ("https://unpkg.com/feather-icons", "dashboards/js/icons.js")

    def get_value(self) -> Any:
        queryset = self.get_queryset()
        queryset = self.aggregate_queryset(queryset)
        return queryset[self.annotated_field_name]

    @classmethod
    def serialize(cls, **kwargs) -> StatSerializerData:
        self = cls()

        return StatSerializerData(
            title=self._meta.verbose_name,
            value=self.get_value(),
            unit=self._meta.unit,
        )

    @classmethod
    def render(cls, **kwargs) -> str:
        value = cls.serialize(**kwargs)
        context = {
            "rendered_value": value,
            **kwargs,
        }

        return render_to_string(cls.template_name, context)


class StatDateChangeSerializer(StatSerializer):
    class Meta(BaseStatSerializer.Meta):
        date_field_name: Optional[str] = None
        previous_delta: Optional[timedelta] = None

    _meta: Type["StatDateChangeSerializer.Meta"]

    def get_date_current(self):
        # only do this if we are set-up with a date field
        if not self._meta.date_field_name:
            return None

        return timezone.now()

    def get_date_previous(self):
        if self._meta.date_field_name is None or self._meta.previous_delta is None:
            return None

        return self.get_date_current() - self._meta.previous_delta

    def get_change_period(self):
        now, previous = self.get_date_current(), self.get_date_previous()
        now += timedelta(seconds=1)
        if previous and now:
            return timesince(previous, now)

        return ""

    @classmethod
    def serialize(cls, **kwargs) -> StatSerializerData:
        self = cls()

        return StatSerializerData(
            title=self._meta.verbose_name,
            value=self.get_value(),
            previous=self.get_previous(),
            unit=self._meta.unit,
            change_period=self.get_change_period(),
        )

    @property
    def date_field(self) -> str:
        if not self._meta.date_field_name:
            return ""

        return f"{self._meta.date_field_name}__lte"

    def get_value(self) -> Any:
        queryset = self.get_queryset()
        date_current = self.get_date_current()
        # filter on date if we have it
        if date_current:
            queryset = queryset.filter(**{self.date_field: date_current})

        queryset = self.aggregate_queryset(queryset)

        return queryset[self.annotated_field_name]

    def get_previous(self) -> Any:
        data_previous = self.get_date_previous()
        # only return previous if we have a previous date to compare
        if data_previous is None:
            return None

        queryset = self.get_queryset()
        queryset = queryset.filter(**{self.date_field: data_previous})
        queryset = self.aggregate_queryset(queryset)

        return queryset[self.annotated_field_name]
