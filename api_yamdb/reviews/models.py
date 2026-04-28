from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from api_yamdb.constants import (
    MAX_LENGHT_NAME_IN_PROJECT,
    MAX_SLUG_IN_PROJECT,
    MAX_SCORE,
    MIN_SCORE,
    MIN_YEAR,
)

from .utils import _current_year


class Category(models.Model):
    """Категория (тип) произведения."""

    name = models.CharField(max_length=MAX_LENGHT_NAME_IN_PROJECT)
    slug = models.SlugField(max_length=MAX_SLUG_IN_PROJECT, unique=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name


class Genre(models.Model):
    """Жанр произведения."""

    name = models.CharField(max_length=MAX_LENGHT_NAME_IN_PROJECT)
    slug = models.SlugField(max_length=MAX_SLUG_IN_PROJECT, unique=True)

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name


class Title(models.Model):
    """Произведение (книга/фильм/музыка), к которому оставляют отзывы."""

    name = models.CharField(max_length=MAX_LENGHT_NAME_IN_PROJECT)
    year = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(
                MIN_YEAR,
                message='Год выпуска не может быть отрицательным'
            ),
            MaxValueValidator(
                _current_year,
                message='Год выпуска не может быть в будующем'
            )
        ],
        verbose_name="Год выпуска",
    )
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="titles",
    )
    genre = models.ManyToManyField(
        Genre,
        related_name="titles",
    )

    class Meta:
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Произведение",
    )
    text = models.TextField(verbose_name="Текст отзыва")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Автор",
    )
    score = models.IntegerField(
        validators=[
            MinValueValidator(MIN_SCORE),
            MaxValueValidator(MAX_SCORE)],
        verbose_name="Оценка",
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата публикации",
    )

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ("-pub_date",)
        constraints = [
            models.UniqueConstraint(
                fields=("title", "author"),
                name="unique_review_per_title_author",
            )
        ]

    def __str__(self) -> str:
        return self.text[:30]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Отзыв",
    )
    text = models.TextField(verbose_name="Текст комментария")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Автор",
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата публикации",
    )

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ("-pub_date",)

    def __str__(self) -> str:
        return self.text[:30]
