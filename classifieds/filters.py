from . import models
import django_filters


class ClassifiedFilter(django_filters.FilterSet):
    class Meta:
        model = models.Classified
        fields = ['aircraft_type']
