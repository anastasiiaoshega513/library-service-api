from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from borrowing.models import Borrowing
from borrowing.serializers import BorrowingListSerializer
from library.tests import sample_book

BORROWING_URL = reverse("borrowing:borrowing-list")


def sample_borrowing(**params):
    defaults = {
        "book": sample_book(),
        "expected_return_date": "2029-03-01",
    }
    defaults.update(params)

    borrowing = Borrowing.objects.create(**defaults)
    return borrowing


def borrowing_detail_url(borrowing_id):
    return reverse("borrowing:borrowing-detail", args=[borrowing_id])


# попытка создать


class GeneralBookApiTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="user@test.com", password="pass1234"
        )

    def test_borrowing_list_forbidden_for_unauthorised(self):
        res = self.client.get(BORROWING_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_sees_only_own_borrowing_list(self):
        other_user = get_user_model().objects.create_user(
            email="other@test.com", password="pass1234"
        )
        book = sample_book()

        own_borrowing = sample_borrowing(user=self.user, book=book)
        other_borrowing = sample_borrowing(user=other_user, book=book)

        self.client.force_authenticate(user=self.user)
        res = self.client.get(BORROWING_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        serializer1 = BorrowingListSerializer(own_borrowing)
        serializer2 = BorrowingListSerializer(other_borrowing)

        self.assertIn(serializer1.data, res.data["results"])
        self.assertNotIn(serializer2.data, res.data["results"])

    def test_borrowing_detail(self):
        self.client.force_authenticate(user=self.user)
        borrowing = sample_borrowing(user=self.user)
        url = borrowing_detail_url(borrowing.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_borrowing_ok(self):
        self.client.force_authenticate(user=self.user)
        payload = {
            "book": sample_book().id,
            "expected_return_date": "2029-03-01",
        }
        res = self.client.post(BORROWING_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
