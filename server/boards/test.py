import json

from rest_framework.test import APITestCase, APIClient

from django.conf import settings

from users.models import User, Profile
from boards.models import Category, Post, Comment, Reply


class BoardTest(APITestCase):
    client = APIClient()
    headers = {}
    
    def setUp(self):
        user = User.objects.create_user('test', 'test@test.com', 'test1234@')
        self.user = user
        profile = Profile(user=user)
        profile.save()
        
        category = Category(title="카테고리", creator=self.user)
        category.save()
        self.category = category
        self.assertIsInstance(category, Category)
        
        post = Post(title="포스트", content="내용", 
                    category=self.category, creator=self.user)
        post.save()
        self.post = post
        self.assertIsInstance(post, Post)
        
        comment = Comment(content="댓글", creator=self.user, post=self.post)
        comment.save()
        self.comment = comment
        self.assertIsInstance(comment, Comment)
        
        reply = Reply(content="대댓글", creator=self.user, comment=self.comment)
        reply.save()
        self.reply = reply
        self.assertIsInstance(reply, Reply)
        
        user = {
            "username": "test",
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
    
    
    ## ==== POST create TEST ALL ====
    def test_create_category(self):
        context = {
            'title': "<script> window.location.href = 'https://hyeo-noo.tistory.com/'; </script>"
        }
        
        response = self.client.post(
            '/api/v1/board/', 
            json.dumps(context), **self.headers, content_type='application/json')
        # print(Category.objects.filter(id=2).first().title)
        self.assertEqual(response.status_code, 201)
    
    
    def test_create_post(self):
        context = {
            'title': '테스트 제목',
            'content': '테스트 내용',
        }
        
        response = self.client.post(
            f'/api/v1/board/{self.category.id}/post', 
            json.dumps(context), **self.headers, content_type='application/json')
        self.assertEqual(response.status_code, 201)
    
    
    def test_create_comment(self):
        context = {
            'content': '댓글',
        }
        
        response = self.client.post(
            f'/api/v1/board/{self.category.id}/post/{self.post.id}/comment', 
            json.dumps(context), **self.headers, content_type='application/json')
        self.assertEqual(response.status_code, 201)
    
    
    def test_create_reply(self):
        context = {
            'content': "대댓글",
        }
        
        response = self.client.post(
            f'/api/v1/board/{self.category.id}/post/{self.post.id}/comment/{self.comment.id}/reply', 
            json.dumps(context), **self.headers, content_type='application/json')
        self.assertEqual(response.status_code, 201)
    
    
    ## ==== GET TEST ALL ====
    def test_show_category(self):
        response = self.client.get(
            f'/api/v1/board/', 
            **self.headers, content_type='application/json')
        self.assertEqual(response.status_code, 200)
    
    def test_show_post(self):
        response = self.client.get(
            f'/api/v1/board/{self.category.id}', 
            **self.headers, content_type='application/json')
        self.assertEqual(response.status_code, 200)
    
    
    ## ==== POST, PUT, DELETE like, modify, delete TEST ALL ====
    def test_modify_reply(self):
        context = {
            'content': "수정된 대댓글",
        }
        
        response = self.client.put(
            f'/api/v1/board/{self.category.id}/post/{self.post.id}/comment/{self.comment.id}/reply/{self.reply.id}', 
            json.dumps(context), **self.headers, content_type='application/json')
        self.assertEqual(response.status_code, 201)
    
    
    def test_like_reply(self):
        response = self.client.post(
            f'/api/v1/board/{self.category.id}/post/{self.post.id}/comment/{self.comment.id}/reply/{self.reply.id}', 
            **self.headers, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        
        
    def test_delete_reply(self):
        response = self.client.delete(
            f'/api/v1/board/{self.category.id}/post/{self.post.id}/comment/{self.comment.id}/reply/{self.reply.id}', 
            **self.headers, content_type='application/json')
        self.assertEqual(response.status_code, 204)
        
        self.reply.delete()
    
    
    def test_modify_comment(self):
        context = {
            'content': "수정된 댓글",
        }
        
        response = self.client.put(
            f'/api/v1/board/{self.category.id}/post/{self.post.id}/comment/{self.comment.id}', 
            json.dumps(context), **self.headers, content_type='application/json')
        self.assertEqual(response.status_code, 201)
    
    
    def test_like_comment(self):
        response = self.client.post(
            f'/api/v1/board/{self.category.id}/post/{self.post.id}/comment/{self.comment.id}', 
            **self.headers, content_type='application/json')
        self.assertEqual(response.status_code, 200)
    
    
    def test_delete_comment(self):
        response = self.client.delete(
            f'/api/v1/board/{self.category.id}/post/{self.post.id}/comment/{self.comment.id}', 
            **self.headers, content_type='application/json')
        self.assertEqual(response.status_code, 204)
        
        self.comment.delete()
    
    
    def test_modify_post(self):
        context = {
            'title': '수정된 제목',
            'content': '수정된 내용',
        }
        
        response = self.client.put(
            f'/api/v1/board/{self.category.id}/post/{self.post.id}',
            json.dumps(context), **self.headers, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        
        
    def test_like_post(self):
        response = self.client.post(
            f'/api/v1/board/{self.category.id}/post/{self.post.id}', 
            **self.headers, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        
        
    def test_delete_post(self):
        response = self.client.delete(
            f'/api/v1/board/{self.category.id}/post/{self.post.id}', 
            **self.headers, content_type='application/json')
        self.assertEqual(response.status_code, 204)
        
        self.post.delete()
    
    
    def test_like_category(self):
        response = self.client.post(
            f'/api/v1/board/{self.category.id}', 
            **self.headers, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        
        
    def test_delete_category(self):
        self.post.delete()
        
        response = self.client.delete(
            f'/api/v1/board/{self.category.id}', 
            **self.headers, content_type='application/json')
        self.assertEqual(response.status_code, 204)
        
        self.category.delete()
    
    