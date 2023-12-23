from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.fields import CharField, EmailField
from rest_framework.serializers import (ModelSerializer, Serializer,
                                        SlugRelatedField)

from api.v1.validators import validator
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        fields = ('username', 'email', 'first_name', 'last_name', 'bio',
                  'role')
        model = User


class UserEditSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        read_only_fields = ('role',)


class SignUpSerializer(Serializer):
    username = CharField(
        max_length=150,
        required=True,
        validators=(validator,),
    )
    email = EmailField(
        max_length=254,
        required=True,
    )

    def validate(self, data):
        email = User.objects.filter(email=data.get('email')).first()
        username = User.objects.filter(username=data.get('username')).first()
        if email != username:
            raise ValidationError('Ошибка')
        return data

    def create(self, validated_data):
        user, created = User.objects.get_or_create(**validated_data)
        user.email_user(
            subject='confirmation_code',
            message=default_token_generator.make_token(user),
        )
        return {
            'email': user.email,
            'username': user.username,
        }


class TokenSerializer(Serializer):
    username = CharField(
        max_length=150,
        required=True,
        validators=(validator,),
    )
    confirmation_code = CharField(required=True)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, data):
        if self.context.get('request').method != 'POST':
            return data
        title_id = self.context['view'].kwargs.get('title_id')
        author = self.context.get('request').user
        title = get_object_or_404(Title, id=title_id)
        if self.context.get('request').method != 'PATCH':
            if title.reviews.filter(author=author).exists():
                raise serializers.ValidationError(
                    'Ваш отзыв уже есть.'
                )
        return data


class CommentSerializer(ModelSerializer):
    author = SlugRelatedField(
        read_only=True,
        slug_field='username')

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class CategoryField(SlugRelatedField):

    def to_representation(self, value):
        return CategorySerializer(value).data


class GenreSerializer(ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')
        ordering = ('name',)


class GenreField(SlugRelatedField):

    def to_representation(self, value):
        return GenreSerializer(value).data


class TitleSerializer(ModelSerializer):
    category = CategoryField(
        queryset=Category.objects.all(),
        required=False,
        slug_field='slug'
    )
    genre = GenreField(
        many=True,
        queryset=Genre.objects.all(),
        required=False,
        slug_field='slug')
    rating = serializers.IntegerField(
        required=False,
        default=None,
        read_only=True
    )

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category')
