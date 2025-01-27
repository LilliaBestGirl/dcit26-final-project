from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from ..models import UserReview, ReviewReception

# Create your tests here.

class UserReviewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        self.review_data = {
            'book': '1',
            'rating': 4,
            'review': 'Great book!',
        }

        self.review_data_2 = UserReview.objects.create(rating=2, review='Not bad, but could be better.', book='/works/OL20008185W', user=self.user)
        self.review_like = ReviewReception.objects.create(review=self.review_data_2, reaction=ReviewReception.LIKE, user=self.user)

        response = self.client.post('/api/token/', {'username': 'testuser', 'password': 'testpassword'}, format='json')
        self.access_token = response.data['access']

    def test_create_review(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.post('/api/user/review/', self.review_data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_get_reviews(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        response = self.client.get('/api/user/review/')
        print(response.data)
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

    def test_book_reviews(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        response = self.client.get('/api/book/review/?key=/works/OL20008185W')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class ReviewReceptionTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        self.review = UserReview.objects.create(rating=5, review='Test review', book='Test book', user=self.user)
        self.review_2 = UserReview.objects.create(rating=5, review='Test review 2', book='Test book 2', user=self.user)

        self.reception = ReviewReception.objects.create(user=self.user, review=self.review, reaction='like')

        response = self.client.post('/api/token/', {'username': 'testuser', 'password': 'testpassword'}, format='json')
        self.access_token = response.data['access']

    def test_like_review(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        response = self.client.post('/api/review/reaction/', {'review': self.review_2.id, 'reaction': 'like'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_reaction(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        response = self.client.post('/api/review/reaction/', {'review': self.review.id, 'reaction': 'dislike'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(ReviewReception.objects.get(user=self.user, review=self.review).reaction)

    def test_cancel_reaction(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        response = self.client.post('/api/review/reaction/', {'review': self.review.id, 'reaction': 'like'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        print(ReviewReception.objects.filter(user=self.user, review=self.review).exists())