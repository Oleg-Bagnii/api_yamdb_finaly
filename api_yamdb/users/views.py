from django.conf import settings
from django.core.mail import send_mail
from django.db import IntegrityError
from rest_framework import status
from rest_framework.decorators import action, api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.tokens import AccessToken

from api.v1.permissions import IsAdminAndAuthenticated
from api.v1.serializers import (SignUpSerializer, TokenSerializer,
                                UserEditSerializer, UserSerializer)
from .models import User


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminAndAuthenticated,)
    filter_backends = (SearchFilter,)
    http_method_names = ('delete', 'get', 'patch', 'post')
    filterset_fields = ('username')
    search_fields = ('username',)
    lookup_field = 'username'

    @action(
        methods=['get', 'patch'],
        detail=False,
        url_path='me',
        permission_classes=(IsAuthenticated,),
        serializer_class=UserEditSerializer,
    )
    def users_author_profile(self, request):
        user = request.user
        if request.method == 'PATCH':
            serializer = UserEditSerializer(
                user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
        else:
            serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def signup(request):
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    email = serializer.validated_data.get('email')
    try:
        User.objects.get_or_create(username=username, email=email)
    except IntegrityError:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    confirmation_code = serializer.validated_data.get('username')
    send_mail('Регистрация',
              f'confirmation_code - {confirmation_code}',
              settings.DEFAULT_FROM_EMAIL,
              [serializer.validated_data.get('email')]
              )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data.get('username')
    )
    if not user.check_password(serializer.validated_data.get('password')):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    token = AccessToken.for_user(user)
    return Response({'token': token.key, 'user': serializer.data})
