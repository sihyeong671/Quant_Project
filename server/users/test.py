import json

from rest_framework.test import APIClient, APITestCase

from users.models import User, Profile


class UserTest(APITestCase):
    
    def test_create_user(self):
        user = User.objects.create_user('TEST', 'test@nav.com', 'test1234@')
        self.assertIsInstance(user, User)
        self.assertFalse(user.is_staff)
        self.assertEqual(user.email, 'test@nav.com')
    
    def test_create_super_user(self):
        user = User.objects.create_superuser('TEST', 'test@nav.com', 'test1234@')
        self.assertIsInstance(user, User)
        self.assertTrue(user.is_staff)
        self.assertEqual(user.email, 'test@nav.com')
    
    
class ProfileTest(APITestCase):
    client = APIClient()
    headers = {}
    
    def setUp(self):
        user = User.objects.create_user('TEST', 'test@nav.com', 'test1234@')
        self.user = user
        profile = Profile(user=user)
        profile.save()
        
        user = {
            "username": "TEST",
            "password": "test1234@"
        }
        
        response = self.client.post('/api/v1/auth/login/', json.dumps(user), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        
        self.token = response.data['access_token']
        self.csrftoken = response.cookies.get('csrftoken').value
        
        self.assertNotEqual(self.token, '')
        
        self.headers = {
            "HTTP_Authorization": "jwt " + self.token,
            "X-CSRFToken": self.csrftoken,
        }
        
    def test_me_api(self):
        
        response = self.client.get(
            '/api/v1/users/me',
            **self.headers, content_type = "application/json")
        self.assertEqual(response.status_code, 200)
        print(response.data)
        
    
    def test_change_password(self):
        context = {
            "oldpassword": "test1234@",
            "newpassword1": "test",
            "newpassword2": "test",
        }
        
        response = self.client.put(
            '/api/v1/users/me',
            json.dumps(context), **self.headers, content_type="application/json")
        self.assertEqual(response.status_code, 200)
    
    
    def test_user_delete(self):
        context = {
            "password": "test1234@"
        }
        
        response = self.client.delete(
            '/api/v1/users/me',
            json.dumps(context), **self.headers, content_type="application/json")
        self.assertEqual(response.status_code, 200)
            
    



# class UserTest(TestCase):
#     client = Client()
#     header = {}
    
#     def setUp(self):
#         User.objects.create_user(username="test", password="1234", email="test@test.com")
    
#     def tearDown(self):
#         user = User.objects.filter(username="test")
#         user.delete()
    
#     def test_login_api(self):
#         user = {
#             'username': 'test',
#             'password': '1234'
#         }
        
#         response = self.client.post('/api/v1/auth/login/', json.dumps(user), content_type='application/json')
#         self.token = response.data['token']
#         self.header = {"Authorization": "jwt " + self.token}
        
#         self.assertEqual(response.status_code, 201)
        
    
#     def test_userme(self):
#         response = self.client.get('/api/v1/users/me', **self.header, content_type='application/json')
#         print(response.data)
        
#         self.assertEqual(response.status_code, 200)
        
#         cate = {
#             'title': '테스트 게시판'
#         }
        
#         board = self.client.post('/api/v1/board/', json.dumps(cate), **self.header, content_type='application/json')
#         self.assertEqual(board.status_code, 201)
        
    