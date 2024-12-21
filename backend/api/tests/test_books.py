from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from ..models import UserReview

class BookTest(APITestCase):

    def setUp(self):
        self.user_1 = User.objects.create_user(username='testuser', password='testpassword')
        self.user_2 = User.objects.create_user(username='testuser2', password='testpassword')
        self.user_3 = User.objects.create_user(username='testuser3', password='testpassword')

        UserReview.objects.create(rating=5, review='Fantastic book!', book='/works/OL34369901W', user=self.user_1)
        UserReview.objects.create(rating=4, review='Meh', book='/works/OL34369901W', user=self.user_2)
        UserReview.objects.create(rating=4, review='Great book!', book='/works/OL34369901W', user=self.user_3)

    def test_get_books(self):
        response = self.client.get('/api/search/?q=learning+python&page=1')

        print(response.data[0])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 20)

    def test_retrieve_book(self):
        response = self.client.get('/api/book/?key=/works/OL34369901W')

        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)