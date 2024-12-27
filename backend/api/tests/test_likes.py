from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from ..models import UserReview, ReviewReception

class ReceptionTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        self.review = UserReview.objects.create(user=self.user, rating=5, review='Test review', book='Test book')
        self.review_2 = UserReview.objects.create(user=self.user, rating=5, review='Test review 2', book='Test book 2')

        self.reception = ReviewReception.objects.create(user=self.user, review=self.review, reaction='like')

        self.access_token = self.client.post('/api/token/', {'username': 'testuser', 'password': 'testpassword'}, format='json').data['access']

    def test_create_reaction(self):
        data = {'review': self.review_2.id, 'reaction': 'like'}
        response = self.client.post('/api/review/reaction/', data, format='json', HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ReviewReception.objects.count(), 2)

    def test_update_reaction(self):
        data = {'review': self.review.id, 'reaction': 'dislike'}
        response = self.client.post('/api/review/reaction/', data, format='json', HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        
        new_reception = ReviewReception.objects.get(user=self.user, review=self.review)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(new_reception.reaction, 'dislike')

    def test_delete_reaction(self):
        response = self.client.delete(f'/api/review/reaction/{self.reception.id}/', HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)