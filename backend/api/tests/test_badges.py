from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from ..models import UserReview, ReviewReception, ObtainedBadge, Badge
from ..utils import get_user_stats, check_and_add_badge

class UserStatsTest(TestCase):
    def setUp(self):
        self.user_1 = User.objects.create_user(username='testuser', password='testpassword')
        self.user_2 = User.objects.create_user(username='testuser2', password='testpassword')

        self.review_1 = UserReview.objects.create(rating=4, review='Great book!', book=1, user=self.user_1)
        self.review_2 = UserReview.objects.create(rating=3, review='Not bad, but could be better.', book=2, user=self.user_1)
        self.review_3 = UserReview.objects.create(rating=5, review='Absolutely loved it!', book=3, user=self.user_1)
        self.review_4 = UserReview.objects.create(rating=2, review='Could have been better.', book=4, user=self.user_2)

        ReviewReception.objects.create(review=self.review_1, reaction=ReviewReception.LIKE, user=self.user_1)
        ReviewReception.objects.create(review=self.review_1, reaction=ReviewReception.LIKE, user=self.user_2)
        ReviewReception.objects.create(review=self.review_2, reaction=ReviewReception.LIKE, user=self.user_1)
        ReviewReception.objects.create(review=self.review_2, reaction=ReviewReception.LIKE, user=self.user_2)
        ReviewReception.objects.create(review=self.review_3, reaction=ReviewReception.DISLIKE, user=self.user_1)
        ReviewReception.objects.create(review=self.review_4, reaction=ReviewReception.DISLIKE, user=self.user_1)

    def test_get_user_stats(self):
        user_stats = get_user_stats(self.user_2)

        print(user_stats)

        self.assertEqual(user_stats['reviews'], 1)
        self.assertEqual(user_stats['likes_given'], 2)
        self.assertEqual(user_stats['dislikes_given'], 0)
        self.assertEqual(user_stats['likes_received'], 0)
        self.assertEqual(user_stats['dislikes_received'], 1)

class UserBadgesTest(APITestCase):
    def setUp(self):
        self.user_1 = User.objects.create_user(username='testuser', password='testpassword')

        Badge.objects.create(badge_name='Test Badge', description='Test badge', condition_type='reviews', tier='bronze', threshold=1)

        response = self.client.post('/api/token/', {'username': 'testuser', 'password': 'testpassword'}, format='json')
        self.access_token = response.data['access']

    def test_badge_obtained(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        
        review_data = {
            'user': self.user_1.id,
            'book': 1,
            'rating': 4,
            'review': 'Great book!'
        }

        response = self.client.post('/api/user/review/', review_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        check_and_add_badge(self.user_1)

        obtained_badges = ObtainedBadge.objects.filter(user=self.user_1)
        self.assertEqual(obtained_badges.count(), 1)
