from datetime import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from acme_project import settings
from users.models import User


class Category(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=settings.NAME_MAX_LENGTH
    )
    slug = models.SlugField(
        verbose_name='Идентификатор',
        max_length=settings.SLUG_MAX_LENGTH,
        unique=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)


class Genre(Category):

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=settings.NAME_MAX_LENGTH
    )
    year = models.IntegerField(
        verbose_name='Дата выхода',
        validators=MaxValueValidator(datetime.now().year)
    )
    description = models.TextField('Описание', blank=True)
    genre = models.ManyToManyField(Genre, through_fields='GenreTitle')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 related_name='categories', null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE)
    genre = models.ForeignKey(
        Genre,
        verbose_name='Жанр',
        on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title}, жанр - {self.genre}'

    class Meta:
        verbose_name = 'Произведение и жанр'
        verbose_name_plural = 'Произведения и жанры'


class Review(models.Model):
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )
    score = models.IntegerField(
        validators=[MaxValueValidator(10), MinValueValidator(1)]
    )

    def __str__(self):
        return self.text[:settings.SLUG_MAX_LENGTH]

    class Meta:
        ordering = ('-pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'),
        ]


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    def __str__(self):
        return self.text[:settings.SLUG_MAX_LENGTH]

    class Meta:
        ordering = ('-pub_date',)
        default_related_name = 'comments'
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
