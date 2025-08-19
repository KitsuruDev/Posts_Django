from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model

User = get_user_model()

class Category(models.Model):
    title = models.CharField(max_length=256, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание")
    slug = models.SlugField(unique=True, blank=True, verbose_name="Идентификатор")  # Auto generate
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Добавлено")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Location(models.Model):
    name = models.CharField(max_length=256, verbose_name="Название места")
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Добавлено")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Местоположение"
        verbose_name_plural = "Местоположения"


class Post(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор публикации"
    )
    title = models.CharField(max_length=256, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Текст")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Категория")
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Местоположение")
    image = models.ImageField(upload_to='images_post/', blank=True, null=True, verbose_name="Изображение")
    published_date = models.DateTimeField(null=True, blank=True, verbose_name="Дата и время публикации", help_text="Если установить дату и время в будущем — можно делать отложенные публикации.")
    is_published = models.BooleanField(default=False, verbose_name="Опубликовано", help_text="Снимите галочку, чтобы скрыть публикацию.")
    views_count = models.PositiveIntegerField(default=0, verbose_name="Количество просмотров")
    slug = models.SlugField(unique=True, blank=True, verbose_name="Идентификатор", help_text="Идентификатор страницы для URL; разрешены символы латиницы, цифры, дефис и подчёркивание.")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Добавлено")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Post.objects.filter(slug=slug).exists():  # Проверяем дубликаты
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Публикация"
        verbose_name_plural = "Публикации"

    @property
    def first_line(self):
        return self.content.split('.')[0]


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_date']

    def __str__(self):
        return f"Комментарий от {self.author.username} в \"{self.post.title}\""