from django.conf import settings
from rest_framework.fields import CharField, EmailField
from rest_framework.serializers import ModelSerializer, Serializer

from api.validators import username_validator
from users.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )
        model = User

    def validate_username(self, value):
        return username_validator(value)


class UserEditSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        read_only_fields = ("role",)


class SignupSerializer(Serializer):
    username = CharField(
        max_length=settings.LIMIT_USERNAME,
        required=True,
        validators=(username_validator,),
    )
    email = EmailField(max_length=settings.LIMIT_EMAIL, required=True)


class TokenSerializer(Serializer):
    username = CharField(
        max_length=settings.LIMIT_USERNAME,
        required=True,
        validators=(username_validator,),
    )
    confirmation_code = CharField(
        max_length=settings.LIMIT_CODE, required=True
    )

    def validate_username(self, value):
        return username_validator(value)
