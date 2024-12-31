#!-*-coding:utf-8-*-
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from reviews.constants import ADMIN_ROLE
from reviews.models import Category, Genre, Review, Title

User = get_user_model()


class TitleRecipeTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Создаем клиента, с токеном.
        cls.admin = User.objects.create(username='lauren', email='l@l.ru', role=ADMIN_ROLE)
        cls.admin.is_superuser = True
        cls.admin.save()

        cls.some_user = User.objects.create(username='some', email='l1@l.ru', role=ADMIN_ROLE)

        # Авторизируем его.
        cls.client_admin = APIClient()
        cls.client_admin.force_authenticate(user=cls.admin)

    def setUp(self):
        self.category = Category.objects.create(name='Sci-fi', slug='sci-fi')
        self.genre = Genre.objects.create(name='Sci-fi', slug='sci-fi')

        self.title = Title.objects.create(
            name='Who',
            description='Who',
            category=self.category,
            year=1999,
        )
        self.review = Review.objects.create(title=self.title, score=5, author=self.admin)
        self.review = Review.objects.create(title=self.title, score=3, author=self.some_user)

    def test_title_detail(self):
        url = reverse('titles-list')

        resp = self.client_admin.get(url)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        print(resp.data)

    def test_title_update(self):
        url = reverse('titles-detail', args=(self.title.id,))

        resp = self.client_admin.patch(url, {'title': 'Where'})

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # print('3   ', resp.data)

    def test_create_title(self):
        url = reverse('titles-list')
        data = {
            'name': 'Doctor Who',
            'year': 2018,
            'genre': self.genre.slug,
            'category': self.category.slug,
        }

        resp = self.client_admin.post(url, data=data)

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # print(resp.data)
