from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from library.models import Book

BOOK_URL = reverse("books-list")


def sample_book(**params):
    defaults = {
        "title": "Test Book",
        "author": "Test Author",
        "cover": "Soft",
        "inventory": 4,
        "daily_fee": 3.00,
    }
    defaults.update(params)

    book = Book.objects.create(**defaults)
    return book


def book_detail_url(book_id):
    return reverse("books-detail", args=[book_id])


class GeneralBookApiTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="user@test.com", password="pass1234"
        )
        self.admin = get_user_model().objects.create_superuser(
            email="admin@test.com", password="pass1234"
        )

    def test_book_list(self):
        res = self.client.get(BOOK_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_book_detail(self):
        book = sample_book()
        url = book_detail_url(book.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_authorised_user_create_book_forbidden(self):
        self.client.force_authenticate(user=self.user)
        payload = {
            "title": "Test Book",
            "author": "Test Author",
            "cover": "Soft",
            "inventory": 4,
            "daily_fee": 3.00,
        }
        res = self.client.post(BOOK_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_create_book_ok(self):
        self.client.force_authenticate(user=self.admin)
        payload = {
            "title": "Test Book",
            "author": "Test Author",
            "cover": "SOFT",
            "inventory": 4,
            "daily_fee": 3.00,
        }
        res = self.client.post(BOOK_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
