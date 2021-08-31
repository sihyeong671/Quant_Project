import json
import jwt

from django.urls import reverse
from django.test import TestCase, Client

from unittest.mock import patch, MagicMock


class AuthTest(TestCase):
    def test_login_api(self):
        client = Client()
        user = {
            'username': 'admin',
            'password': 'admin'
        }

        response = client.post('/api/v1/auth/login/', json.dumps(user), content_type='application/json')
        self.assertEqual(response.status_code, 201)
    