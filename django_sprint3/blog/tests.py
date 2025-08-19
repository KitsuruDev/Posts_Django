from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Post, Category, Location

User = get_user_model()

class PostCreateViewTest(TestCase):
    def setUp(self):
        """Создаем пользователя"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.client.login(username='testuser', password='testpassword')  # Аутентификация пользователя
        self.post_create_url = reverse('blog:post_create') # Получаем URL для создания поста
        self.category = Category.objects.create(title='Новости', description='Описание') # создаём категорию
        self.location = Location.objects.create(name='Москва') # создаём локацию

    def test_post_create_view(self):
        """Тестируем создание поста через view"""
        data = {
            'title': 'Новый тестовый пост',
            'content': 'Содержание нового тестового поста',
            'category': str(self.category.pk),
            'location': str(self.location.pk),
            'published_date': '2024-06-15 14:30:00',
            'slug': 'testovayazapis'
        }
        response = self.client.post(self.post_create_url, data) # отправляем пост
        self.assertEqual(response.status_code, 302)  # Проверяем редирект (302 - это статус редиректа)
        self.assertEqual(Post.objects.count(), 1)  # Проверяем, что пост был создан
        post = Post.objects.first()  # получаем первую строку поста
        self.assertEqual(post.title, 'Новый тестовый пост') # Проверяем название поста
        self.assertEqual(post.author, self.user)  # Проверяем, что автор поста - это созданный пользователь
