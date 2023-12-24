from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.filters import SearchFilter
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import AccessToken

from api.v1.filters import TitleFilter
from api.v1.permissions import (IsAdminAndAuthenticated,
                                IsAdminOrAuthorOrReadOnly, IsAdminOrReadOnly)
from api.v1.serializers import (CategorySerializer, CommentSerializer,
                                GenreSerializer, ReviewSerializer,
                                SignUpSerializer, TitleSerializer,
                                TokenSerializer, UserEditSerializer,
                                UserSerializer)
from reviews.models import Category, Genre, Review, Title

User = get_user_model()


class UserTitleReviewCommentBase(viewsets.ModelViewSet):
    http_method_names = ('delete', 'get', 'patch', 'post')


class UserViewSet(UserTitleReviewCommentBase):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminAndAuthenticated,)
    filter_backends = (SearchFilter,)
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
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data.get('username')
    )
    confirmation_code = serializer.validated_data.get('confirmation_code')
    if not default_token_generator.check_token(user, confirmation_code):
        mesage = {'confirmation_code': 'Невалиден код подтверждения'}
        return Response(mesage, status=status.HTTP_400_BAD_REQUEST)
    token = AccessToken.for_user(user)
    return Response({'token': str(token)})


class CreateDestroyListCategoryGenre(
        GenericViewSet,
        CreateModelMixin,
        DestroyModelMixin,
        ListModelMixin
):
    filter_backends = (SearchFilter,)
    lookup_field = 'slug'
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly,)


class TitleViewSet(UserTitleReviewCommentBase):
    queryset = Title.objects.annotate(rating=Avg('reviews__score')
                                      ).order_by('name')
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter


class CategoryViewSet(CreateDestroyListCategoryGenre):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CreateDestroyListCategoryGenre):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ReviewCommentPermissionsBase(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrAuthorOrReadOnly,)


class ReviewViewSet(UserTitleReviewCommentBase, ReviewCommentPermissionsBase):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def __get_title(self):
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Title, id=title_id)

    def get_queryset(self):
        return self.__get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.__get_title())


class CommentViewSet(UserTitleReviewCommentBase, ReviewCommentPermissionsBase):
    serializer_class = CommentSerializer

    def __get_review(self, get_data):
        return get_object_or_404(Review, pk=get_data.get('review_id'),
                                 title_id=get_data.get('title_id'))

    def get_queryset(self):
        return self.__get_review(get_data=self.kwargs).comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.__get_review(get_data=self.kwargs))
