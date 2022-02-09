from django_filters import FilterSet, NumberFilter
from .models import Client
from django.db.models import Q
from .utils.great_circle_distance import get_great_circle_distance


class ClientFilter(FilterSet):
    distance = NumberFilter(method='filter_distance')

    class Meta:
        model = Client
        fields = ('name', 'surname', 'gender', 'distance')

    def filter_distance(self, queryset, value, distance):
        client = self.request.auth.user
        clients_filtered_by_distance = []
        client_latitude = client.latitude
        client_longitude = client.longitude
        if not Client.objects.filter(Q(id=client.id) & ~Q(latitude=None) & ~Q(longitude=None)):
            raise ValueError({'error': 'Одно из полей (широта иил долгота) отсутсвует в базе данных'})
        if value:
            queryset = Client.objects.filter(~Q(id=client.id) & ~Q(latitude=None) & ~Q(longitude=None))
            for client in queryset:
                if get_great_circle_distance((client_latitude, client_longitude), (client.latitude, client.longitude),
                                             distance):
                    clients_filtered_by_distance.append(client.id)
        return Client.objects.filter(id__in=clients_filtered_by_distance)
