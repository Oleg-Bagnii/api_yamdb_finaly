from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import GenericViewSet

from api.filters import TitleFilter
from api.permissions import IsAdminOrAuthorOrReadOnly, IsAdminOrReadOnly
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, ReviewSerializer,
                             TitleSerializer)
from reviews.models import Category, Genre, Review, Title


class CreateDestroyList(
        GenericViewSet, CreateModelMixin, DestroyModelMixin, ListModelMixin):
    pass


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    http_method_names = ('delete', 'get', 'patch', 'post')
    filterset_class = TitleFilter


class CategoryViewSet(CreateDestroyList):
    filter_backends = (SearchFilter,)
    lookup_field = 'slug'
    search_fields = ('name',)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination


class GenreViewSet(CreateDestroyList):
    filter_backends = (SearchFilter,)
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)
    search_fields = ('name',)
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminOrAuthorOrReadOnly,)
    http_method_names = ('delete', 'get', 'patch', 'post')

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAdminOrAuthorOrReadOnly,)
    http_method_names = ('delete', 'get', 'patch', 'post')

    def __get_review(self, get_data):
        return get_object_or_404(Review, pk=get_data.get('review_id'))

    def get_queryset(self):
        return self.__get_review(get_data=self.kwargs).comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.__get_review(get_data=self.kwargs))
