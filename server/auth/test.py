import json

from rest_framework.test import APITestCase, APIClient

from users.models import User, Profile


class AuthTest(APITestCase):
    
    def setUp(self):
        user = User.objects.create_user('test', 'test@test.com', 'test')
        self.user = user
        profile = Profile(user=user)
        profile.save()
        
        
    def test_login_api(self):
        client = APIClient()
        user = {
            'username': 'test',
            'password': 'test'
        }

        response = client.post('/api/v1/auth/login/', json.dumps(user), content_type='application/json')
        
        print(response)
        
        self.assertEqual(response.status_code, 200)
        
    