import django_filters
from .models import Samples


class SampleFilter(django_filters.FilterSet):
    class Meta:
        model = Samples
        fields = ['set_id', 'name']