from django.contrib.auth.models import User, Group
from .models import Event, CustomUser
from django.conf import settings
from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer
from rest_auth.models import TokenModel
from allauth.account.adapter import get_adapter

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class UserSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    events = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all(), many=True)
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'username', 'events', 'organization', 'points',)

class CustomRegisterSerializer(RegisterSerializer):
    organization = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'password', 'organization')

    def get_clean_data(self):
        return {
                'username': self.validate_data.get('username', ''),
                'password1': self.validate_data.get('password1', ''),
                'password2': self.validate_data.get('password2', ''),
                'email': self.validate_data.get('email', ''),
                'organization': self.validate_Data.get('organization', '')
        }

        def save(self, request):
            adapter = get_adapter()
            user = adapter.new_user(request)
            self.cleaned_data = self.get_clean_data()
            user.organization = self.cleaned_data.get('organization')
            user.save()
            adapter.save_user(request, user, self)
            return user

class EventSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    user_list = UserSerializer(many=True, read_only=True)
    class Meta:
        model = Event
        fields = ['id', 'name', 'time', 'place', 'points', 'code', 'description', 'user_list']

class TokenSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = TokenModel
        fields = ['key', 'user']
