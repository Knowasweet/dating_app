from django.urls import path
from .views import *

app_name = 'dating'

clients_create = ClientRegistrationView.as_view({'post': 'create'})
urlpatterns = [
    path('clients/create', clients_create, name='register'),
]
