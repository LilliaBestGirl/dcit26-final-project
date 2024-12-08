from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from ..models import UserReview, ReviewReception
from ..utils import get_user_stats

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