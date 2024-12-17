from rest_framework.test import APITestCase
from rest_framework import status

class BookTest(APITestCase):
    def test_get_books(self):
        response = self.client.get('/api/search/?q=learning+python&page=1')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 20)