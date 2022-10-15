import shutil
import tempfile


from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.conf import settings
from ..models import Group, Post, Follow
from django import forms
from django.core.cache import cache


User = get_user_model()

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


class TaskPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='neo')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
            group=cls.group,
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def param(self, args):
        return args.author, args.text, args.group

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_pages_names = {
            reverse('posts:main'): 'posts/index.html',
            reverse('posts:group_posts', kwargs={'slug': 'test-slug'}):
                'posts/group_list.html',
            reverse('posts:profile', kwargs={'username': 'neo'}):
                'posts/profile.html',
            reverse('posts:post_detail', kwargs={'post_id': self.post.id}):
                'posts/post_detail.html',
            reverse('posts:post_create'): 'posts/create.html',
            reverse('posts:post_edit', kwargs={'post_id': self.post.id}):
                'posts/create.html',
        }

        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_home_page_show_correct_context(self):
        """Шаблон home сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:main'))
        first_object = response.context['page_obj'][0]
        self.assertEqual(self.param(first_object), self.param(self.post))

    def test_group_posts_page_show_correct_context(self):
        """Шаблон group_posts сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:group_posts', kwargs={'slug': 'test-slug'})
        )
        first_object = response.context['page_obj'][0]
        post_list = Post.objects.filter(group=self.group)[0]
        self.assertEqual(self.param(first_object), self.param(post_list))

    def test_profile_page_show_correct_context(self):
        """Шаблон profile сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:profile', kwargs={'username': 'neo'})
        )
        first_object = response.context['page_obj'][0]
        post_list = Post.objects.filter(author=self.user)[0]
        self.assertEqual(self.param(first_object), self.param(post_list))

    def test_post_detail_page_show_correct_context(self):
        """Шаблон home сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:post_detail', kwargs={'post_id': self.post.id})
        )
        first_object = response.context['post']
        post_list = Post.objects.get(id=self.post.id)
        self.assertEqual(self.param(first_object), self.param(post_list))

    def test_correct_form(self):
        """Шаблоны post_edit и post_create
        сформированы с правильным контекстом."""
        templates_pages_names = [
            reverse('posts:post_edit', kwargs={'post_id': self.post.id}),
            reverse('posts:post_create'),
        ]
        for reverse_name in templates_pages_names:
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertIsInstance(
                    response.context['form'], forms.ModelForm)


class TaskPaginatorTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='neo')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        bulk_list = [
            Post(author=cls.user, text='Тестовый пост', group=cls.group)
            for _ in range(13)
        ]
        cls.post = Post.objects.bulk_create(bulk_list)

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_paginator(self):
        """Тестируем работу пагинатора."""
        templates_pages_names = [
            reverse('posts:main'),
            reverse('posts:group_posts', kwargs={'slug': self.group.slug}),
            reverse('posts:profile', kwargs={'username': self.user}),
        ]
        for reverse_name in templates_pages_names:
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertEqual((len(response.context['page_obj'])), 10)

        for reverse_name in templates_pages_names:
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get((reverse_name)
                                                      + '?page=2')
                self.assertEqual((len(response.context['page_obj'])), 3)


class TaskNewPostTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='neo')
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
            group=Group.objects.create(
                title='Тестовая группа',
                slug='test-slug',
                description='Тестовое описание',
            ))

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_new_post_show_correct_context(self):
        """Проверяем что при создании поста он отображается
        на нужных страницах"""
        self.post = Post.objects.create(
            author=self.user,
            text='Тестовый пост2',
            group=Group.objects.create(
                title='Тестовая группа2',
                slug='test2-slug',
                description='Тестовое описание',
            ))
        templates_pages_names = [
            reverse('posts:main'),
            reverse('posts:group_posts', kwargs={'slug': 'test2-slug'}),
            reverse('posts:profile', kwargs={'username': self.user}),
        ]
        for reverse_name in templates_pages_names:
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                first_object = response.context['page_obj'][0]
                self.assertEqual(first_object.text, self.post.text)

    def test_new_post_show_correct_other_group(self):
        """Пост не попал в группу для которой не предназначен."""
        self.post = Post.objects.create(
            author=self.user,
            text='Тестовый пост2',
            group=Group.objects.create(
                title='Тестовая группа2',
                slug='test2-slug',
                description='Тестовое описание',
            ))
        response = self.authorized_client.get(
            reverse('posts:group_posts', kwargs={'slug': 'test-slug'})
        )
        first_object = response.context['page_obj'][0]
        self.assertNotEqual(first_object.group, self.post.group)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class TaskImageTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='neo')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
            group=cls.group,
            image=uploaded
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_image_task(self):
        """Тестируем что изобраение передается на нужные страницы"""
        templates_pages_names = [
            reverse('posts:main'),
            reverse('posts:profile', kwargs={'username': self.user}),
            reverse('posts:group_posts', kwargs={'slug': 'test-slug'}),
        ]
        for reverse_name in templates_pages_names:
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                first_object = response.context['page_obj'][0]
                self.assertEqual(first_object.image, self.post.image)

        response = self.authorized_client.get(reverse(
            'posts:post_detail', kwargs={'post_id': self.post.id}))
        object = response.context['post']
        self.assertEqual(object.image, self.post.image)


class TaskCacheTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='neo')
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_cache_task(self):
        """Проверяем корректную работу кеша"""
        response_one = self.authorized_client.get(reverse('posts:main'))
        self.post.delete()
        response_two = self.authorized_client.get(reverse('posts:main'))
        cache.clear()
        response_three = self.authorized_client.get(reverse('posts:main'))
        self.assertEqual(response_one.content, response_two.content)
        self.assertNotEqual(response_one.content, response_three.content)


class FollowingTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='neo')
        cls.user2 = User.objects.create_user(username='leo')
        cls.user3 = User.objects.create_user(username='areo')
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client2 = Client()
        self.authorized_client3 = Client()
        self.authorized_client.force_login(self.user)
        self.authorized_client2.force_login(self.user2)
        self.authorized_client3.force_login(self.user3)

    def test_following_task(self):
        """Авторизированный позльзователь может подписываться
        на авторов и удалять подписки."""
        self.authorized_client.post(reverse(
            'posts:profile_follow',
            kwargs={'username': self.user2}))
        self.assertEqual(Follow.objects.get().author, self.user2)
        self.authorized_client.post(reverse(
            'posts:profile_unfollow',
            kwargs={'username': self.user2}))
        follow_count = Follow.objects.count()
        self.assertEqual(follow_count, 0)

    def test_following_correct_task(self):
        """Новая запись пользователя появляется в ленте тех,
         кто на него подписан."""
        self.authorized_client2.post(reverse(
            'posts:profile_follow',
            kwargs={'username': self.user}))
        self.authorized_client.post(
            reverse('posts:post_create'),
            {
                'text': 'Тестовый пост 2222',
                'author': self.user,
            }
        )
        response = self.authorized_client2.get(reverse(
            'posts:follow_index'))
        object = response.context['page_obj']
        self.assertEqual(len(object), 2)
        response = self.authorized_client3.get(reverse(
            'posts:follow_index'))
        object = response.context['page_obj']
        self.assertEqual(len(object), 0)

    def test_following_once_task(self):
        """Проверяем что подписаться можно
        только один раз"""
        self.authorized_client.post(reverse(
            'posts:profile_follow',
            kwargs={'username': self.user2}))
        follow_count1 = Follow.objects.count()
        self.authorized_client.post(reverse(
            'posts:profile_follow',
            kwargs={'username': self.user2}))
        follow_count2 = Follow.objects.count()
        self.assertEqual(follow_count1, follow_count2)
