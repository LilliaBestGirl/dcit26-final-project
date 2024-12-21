from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from ..models import UserReview

# Create your tests here.

class UserReviewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        self.review_data = {
            'book': '1',
            'rating': 4,
            'review': 'Great book!'
        }

        self.review_data_2 = UserReview.objects.create(rating=2, review='Not bad, but could be better.', book='2', user=self.user)

        response = self.client.post('/api/token/', {'username': 'testuser', 'password': 'testpassword'}, format='json')
        self.access_token = response.data['access']

    def test_create_review(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.post('/api/user/review/', self.review_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_get_reviews(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        response = self.client.get('/api/user/review/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_review(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        response = self.client.get('/api/user/review/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_review(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        self.updated_data = {
            'rating': 3,
            'review': 'EDIT: changed my mind, it\'s actually not that bad.',
            'book': '2',
            'user': self.user.id,
        }

        response = self.client.put('/api/user/review/1/', self.updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        review = UserReview.objects.get(id=1)
        self.assertEqual(review.rating, 3)
        self.assertEqual(review.review, 'EDIT: changed my mind, it\'s actually not that bad.')

    def test_delete_review(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        response = self.client.delete('/api/user/review/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)