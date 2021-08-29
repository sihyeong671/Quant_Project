import json
import jwt

from django.urls import reverse
from django.test import TestCase, Client

from users.models import User

class BoardTest(TestCase):
    client = Client()
    header = {}
    
    def setUp(self):
        User.objects.create_user(username="test", password="1234", email="test@test.com")
        user = {
            "username": "test",
            "password": "1234"
        }
        response = self.client.post('/api/v1/auth/login/', json.dumps(user), content_type='application/json')
        self.token = response.data['token']
        self.header = {"Authorization": "jwt " + self.token}
        
        self.assertEqual(response.status_code, 201)
        
    
    def tearDown(self):
        user = User.objects.filter(username="test")
        user.delete()
        
    
    def test_userme(self):
        cate = {
            'title': '테스트 게시판'
        }
        
        response = self.client.post('/api/v1/board/', json.dumps(cate), **self.header, content_type='application/json')
        print(response.data)
        self.assertEqual(response.status_code, 201)
        
    