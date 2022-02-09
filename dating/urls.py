from django.urls import path
from .views import *

app_name = 'dating'

clients_create = ClientRegistrationView.as_view({'post': 'create'})
clients_match = ClientMatchView.as_view({'post': 'create'})
clients_list = ClientListView.as_view({'get': 'list'})
urlpatterns = [
    path('clients/create', clients_create, name='register'),
    path('clients/<int:pk>/match', clients_match, name='match'),
    path('list', clients_list, name='list'),
]
