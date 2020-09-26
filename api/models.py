from django.contrib.auth import get_user_model
from django.db import models
from statistics import mean

from django.shortcuts import get_object_or_404

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=100)
    year = models.IntegerField()
    rating = models.IntegerField()
    description = models.CharField(max_length=500)
    genre = models.ManyToManyField(Genre)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name="category",
        blank=True,
        null=True,
        verbose_name='Категория'
    )

    def __str__(self):
        return self.name

    def get_rating(self):
        title = get_object_or_404(Title, id=self.pk)
        if title.reviews.all():
            self.rating = mean(title.reviews.all())
        else:
            self.rating = 0
        return self.rating
