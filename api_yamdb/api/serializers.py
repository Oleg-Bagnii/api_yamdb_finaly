from api.validators import username_validator
from django.conf import settings
from rest_framework.fields import CharField, EmailField, SerializerMethodField
from rest_framework.serializers import ModelSerializer, Serializer

from reviews.models import Review, Comment, Title, Genre, Category
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


class ReviewSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('product',)


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('review',)


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class GenreSerializer(ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class TitleSerializer(ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = SerializerMethodField()

    class Meta:
        model = Title
        fields = ('id', 'name', 'rating', 'description', 'genre', 'category',)

    def get_rating(self, request, obj):
        reviews = Review.objects.filter(product=request.product)
        rating = 0
        for review in reviews:
            rating = rating + review.score
        return rating / len(reviews)
