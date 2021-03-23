from . import models
import django_filters


class ClassifiedFilter(django_filters.FilterSet):
    class Meta:
        model = models.Classified
        fields = {
            'price_usd':['gte','lte'],
            'year_of_make':['gte','lte'],
            'aircraft_make__make_name':['exact'],
            'aircraft_type__type_name':['exact']
        }
