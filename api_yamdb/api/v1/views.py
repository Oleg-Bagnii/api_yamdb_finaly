from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.viewsets import GenericViewSet

from api.v1.filters import TitleFilter
from api.v1.permissions import IsAdminOrAuthorOrReadOnly, IsAdminOrReadOnly
from api.v1.serializers import (CategorySerializer, CommentSerializer,
                                GenreSerializer, ReviewSerializer,
                                TitleSerializer)
from reviews.models import Category, Genre, Review, Title


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


class TitleReviewCommentBase(viewsets.ModelViewSet):
    http_method_names = ('delete', 'get', 'patch', 'post')


class TitleViewSet(TitleReviewCommentBase):
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


class ReviewViewSet(TitleReviewCommentBase, ReviewCommentPermissionsBase):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def __get_title(self):
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Title, id=title_id)

    def get_queryset(self):
        return self.__get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.__get_title())


class CommentViewSet(TitleReviewCommentBase, ReviewCommentPermissionsBase):
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
