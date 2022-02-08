from rest_framework import status
from rest_framework.response import Response
from .serializers import ClientRegistrationSerializer
from rest_framework import viewsets
from .models import Client
from rest_framework.authtoken.models import Token


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
