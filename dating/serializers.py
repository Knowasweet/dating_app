from rest_framework import serializers
from .models import Client


class ClientRegistrationSerializer(serializers.ModelSerializer):
    gender = serializers.ChoiceField(choices=Client.gender_choices,
                                     error_messages={'invalid_choice': 'Введите m(male) или f(female)'})

    class Meta:
        model = Client
        fields = '__all__'

    def create(self, validated_data):
        client = Client.objects.create_user(
            email=validated_data.get('email'),
            password=validated_data.get('password'),
            name=validated_data.get('name'),
            surname=validated_data.get('surname'),
            gender=validated_data.get('gender'),
            avatar=validated_data.get('avatar'),
        )
        return client
