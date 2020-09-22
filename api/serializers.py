from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from .custom_authentication import AuthenticationWithoutPassword
from .models import User


class UserAllSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', )


class TokenObtainPairWithoutPasswordSerializer(TokenObtainPairSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request_code = kwargs['data']['confirmation_code']
        self.fields['password'].required = False

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
        }
        try:
            authenticate_kwargs['request'] = self.context['request']
        except KeyError:
            pass
        self.user = AuthenticationWithoutPassword().authenticate(**authenticate_kwargs)
        if self.user.confirmation_key != self.request_code:
            data = {'error': 'confirmation_code is not valid'}
        else:
            refresh = self.get_token(self.user)
            data = {'token': str(refresh.access_token)}
        return data

