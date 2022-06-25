from rest_framework import serializers

from .models import User, Account
from . import google
from django.contrib.auth.hashers import make_password


class AccountSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class AccountGGSerializer(serializers.Serializer):
    class Meta:
        models = Account
        fields = ['usename', 'id']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'avatar', 'full_name', 'address', 'total_money', 'currency_unit']


class MoneySerializer(serializers.ModelSerializer):
    total_money = serializers.DecimalField(max_digits=15, decimal_places=0)


class RegisterUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    avatar = serializers.CharField()
    password = serializers.CharField()
    full_name = serializers.CharField()
    address = serializers.CharField()
    total_money = serializers.DecimalField(max_digits=15, decimal_places=0)

    @staticmethod
    def validate_password(password: str) -> str:
        return make_password(password)


class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = google.Google.validate(auth_token)
        try:
            user_data['sub']
        except:
            raise serializers.ValidationError(
                'The token is invalid or expired. Please login again.'
            )
        if user_data['email_verified']:
            return user_data
        return None

    # def custom_token_generator(request, refresh_token=False):
    #     client_code = request.user and request.user.client.codigo
    #
    #     now = datetime.now()
    #     payload = {
    #         'iat': int(now.timestamp()),
    #         'exp': int(expires.timestamp()),
    #     }
    #     if client_code:
    #         payload['org'] = client_code
    #     return jwt.encode(payload, settings.JWT['EC_PRIVATE_KEY'].encode(), algorithm='ES256').decode('ascii')
