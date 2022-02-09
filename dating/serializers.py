from rest_framework import serializers
from .models import Client, Sympathy


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


class ClientMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('id',)

    def validate(self, attrs):
        client_liked_id = self.initial_data['client_liked_id']
        client_id = self.initial_data['client_id']
        if not Client.objects.filter(pk=client_liked_id).exists():
            raise serializers.ValidationError({'error': 'Клиент не существует'})
        if client_id == client_liked_id:
            raise serializers.ValidationError({'error': 'Нельзя выбрать самого себя'})
        if Sympathy.objects.filter(client_id=client_id, client_liked_id=client_liked_id).exists():
            raise serializers.ValidationError({'error': 'Вы проявили уже симпатию'})
        return attrs

    def create(self, validated_data):
        sympathy = Sympathy.objects.create(
            client_id=self.initial_data['client_id'],
            client_liked_id=self.initial_data['client_liked_id']
        )
        return sympathy


class ClientListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('email', 'name', 'surname', 'gender', 'avatar',)
