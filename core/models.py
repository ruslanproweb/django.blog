from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.urls import reverse



# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'  # Отображение названия модели в единственном числе
        verbose_name_plural = 'Категории'  # Отображение названия модели в можественном числе


class Article(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название', unique=True)
    short_description = models.TextField(max_length=150, verbose_name='Краткое описание')
    full_description = models.TextField(verbose_name='Полное описание')
    image = models.ImageField(verbose_name='Фото', upload_to='articles/', blank=True, null=True)
    views = models.PositiveSmallIntegerField(default=0, verbose_name='Просмотры')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')

    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'article_id': self.pk})

    def display_image_in_admin(self):
        if not self.image:
            return ''
        return mark_safe(f'<img src="{self.image.url}" width="100" height="100">')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


# Comment
# author
# article
# created_at
# text
# Comment object (1)

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Статья')
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField(verbose_name='Текст отзыва')

    def __str__(self):
        return f'{self.author}: {self.article}'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Like(models.Model):
    user = models.ManyToManyField(User, related_name='likes')
    article = models.OneToOneField(Article, on_delete=models.CASCADE, related_name='likes', blank=True, null=True)
    comment = models.OneToOneField(Comment, on_delete=models.CASCADE, related_name='likes', blank=True, null=True)


class Dislike(models.Model):
    user = models.ManyToManyField(User, related_name='dislikes')
    article = models.OneToOneField(Article, on_delete=models.CASCADE, related_name='dislikes', blank=True, null=True)
    comment = models.OneToOneField(Comment, on_delete=models.CASCADE, related_name='dislikes', blank=True, null=True)