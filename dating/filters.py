from django_filters import FilterSet
from .models import Client


class ClientFilter(FilterSet):
    class Meta:
        model = Client
        fields = ('name', 'surname', 'gender',)
