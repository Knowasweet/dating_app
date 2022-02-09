from rest_framework import status
from rest_framework.response import Response
from .filters import ClientFilter
from .serializers import ClientRegistrationSerializer, ClientMatchSerializer, ClientListSerializer
from rest_framework import viewsets
from .models import Client, Sympathy
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core.mail import EmailMessage
from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend


class ClientRegistrationView(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        token = Token.objects.create(user_id=serializer.data['id'])
        serializer.data['token'] = token.key
        return Response({'success': 'True', 'token': f'{token.key}'}, status=status.HTTP_201_CREATED, headers=headers)


class ClientMatchView(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientMatchSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def create(self, request, *args, **kwargs):
        request.data['client_liked_id'] = kwargs['pk']
        request.data['client_id'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        if Sympathy.objects.filter(client_id=request.user.id,
                                   client_liked_id=kwargs['pk']).exists() and Sympathy.objects.filter(
                client_id=kwargs['pk'], client_liked_id=request.user.id).exists():
            client_liked = Client.objects.get(id=kwargs['pk'])
            client = EmailMessage(subject='Сайт знакомств',
                                  body=f'«Вы понравились {client_liked.name}! Почта участника: {client_liked}».',
                                  from_email=settings.EMAIL_FROM_USER, to=[request.user.email])
            client_liked = EmailMessage(subject='Сайт знакомств',
                                        body=f'«Вы понравились {request.user.name}! Почта участника: {request.user.email}».',
                                        from_email=settings.EMAIL_FROM_USER, to=[client_liked])
            client.send()
            client_liked.send()
            return Response({'success': 'True',
                             'message': f'Поздравляем, у вас взаимная симпатия, см. в email {request.user.email}'},
                            status=status.HTTP_200_OK, headers=headers)
        else:
            return Response({'success': 'True',
                             'message': 'Вы проявили симпатию. Вас оповестят в почте, если возникнет взаимная симпатия'},
                            status=status.HTTP_200_OK, headers=headers)


class ClientListView(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ClientFilter
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
