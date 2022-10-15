from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from ..models import Group, Post


User = get_user_model()


class TaskURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_1 = User.objects.create_user(username='neo')
        cls.user_2 = User.objects.create_user(username='leo')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user_1,
            text='Тестовый пост',
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client_1 = Client()
        self.authorized_client_1.force_login(self.user_1)
        self.authorized_client_2 = Client()
        self.authorized_client_2.force_login(self.user_2)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""

        templates_url_names = {
            '/': 'posts/index.html',
            f'/group/{self.group.slug}/': 'posts/group_list.html',
            f'/profile/{self.user_1}/': 'posts/profile.html',
            f'/posts/{self.post.id}/': 'posts/post_detail.html',
            f'/posts/{self.post.id}/edit/': 'posts/create.html',
            '/create/': 'posts/create.html',
        }

        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = self.authorized_client_1.get(address)
                self.assertTemplateUsed(response, template)

    def test_url_exists_authorized_client(self):
        """Проверяем доступность URL-адресов авторизированному пользователю."""
        list_url = [
            '/',
            f'/group/{self.group.slug}/',
            f'/profile/{self.user_1}/',
            f'/posts/{self.post.id}/',
            '/create/',
        ]
        for address in list_url:
            with self.subTest(address=address):
                response = self.authorized_client_1.get(address)
                self.assertEqual(response.status_code, HTTPStatus.OK.value)

    def test_url_exists_guest(self):
        """Проверяем недоступность URL-адресов
        неавторизированному пользователю."""
        list_url = [
            f'/posts/{self.post.id}/edit/',
            '/create/',
            f'/posts/{self.post.id}/comment/'
        ]
        for address in list_url:
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertEqual(response.status_code, HTTPStatus.FOUND.value)

    def test_unexisting_page(self):
        """Тест несуществующей страницы."""
        response = self.authorized_client_1.get('/unexisting_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND.value)

    def test_url_exists_author(self):
        """Проверяем что доступ к редактированию поста есть только у автора."""
        response = self.authorized_client_2.get(f'/posts/{self.post.id}/edit/')
        self.assertEqual(response.status_code, HTTPStatus.FOUND.value)
