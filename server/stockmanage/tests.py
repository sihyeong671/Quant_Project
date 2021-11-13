import json

from rest_framework.test import APITestCase, APIClient

from users.models import Profile, User
from stockmanage.models import Company


class StockApitest(APITestCase):
    client = APIClient()
    headers = {}
    
    def setUp(self):
        user = User.objects.create_user('test', 'test@test.com', 'test')
        self.user = user
        profile = Profile(user=user)
        profile.save()
        
        company = Company(corp_name="test회사")
        company.save()
        self.company = company
        self.assertIsInstance(company, Company)
        
        user = {
            "username": "test",
            "password": "test"
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
    
    
    ## ==== stock API TEST ====
    
    ## 재무제표의 내용을 임의로 추가하기가 어려워 웬만한 api는 postman에서 테스트를 진행함.
    def test_get_companyname(self):
        
        response = self.client.get(
            '/api/v1/stock/company',  **self.headers, content_type='application/json')
        
        print(response.data)
        self.assertEqual(response.status_code, 200)
    