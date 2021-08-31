import json
import jwt

from rest_framework.test import APITestCase, APIClient

from django.conf import settings

from users.models import User
from boards.models import Category, Post, Comment, Reply

class BoardTest(APITestCase):
    client = APIClient()
    header = {}
    
    def setUp(self):
        user = User.objects.create_user('test', 'test@test.com', 'test1234@')
        self.user = user
        self.assertIsInstance(user, User)
        
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
        self.assertEqual(response.status_code, 201)
        
        self.token = response.data['token']
        self.assertNotEqual(self.token, '')
        
        self.header = {"Authorization": "jwt " + self.token}
        
    
    def test_create_category(self):
        context = {
            'title': '테스트 게시판'
        }
        
        response = self.client.post(
            '/api/v1/board/', 
            json.dumps(context), **self.header, content_type='application/json')
        self.assertEqual(response.status_code, 201)
    
    
    def test_create_post(self):
        context = {
            'title': '테스트 제목',
            'content': '테스트 내용',
        }
        
        response = self.client.post(
            f'/api/v1/board/{self.category.id}/post', 
            json.dumps(context), **self.header, content_type='application/json')
        self.assertEqual(response.status_code, 201)
    
    
    def test_create_comment(self):
        context = {
            'content': '댓글',
        }
        
        response = self.client.post(
            f'/api/v1/board/{self.category.id}/post/{self.post.id}/comment', 
            json.dumps(context), **self.header, content_type='application/json')
        self.assertEqual(response.status_code, 201)
    
    
    def test_create_reply(self):
        context = {
            'content': "대댓글",
        }
        
        response = self.client.post(
            f'/api/v1/board/{self.category.id}/post/{self.post.id}/comment/{self.comment.id}/reply', 
            json.dumps(context), **self.header, content_type='application/json')
        self.assertEqual(response.status_code, 201)
    
    
    def test_modify_reply(self):
        context = {
            'content': "수정된 대댓글",
        }
        
        response = self.client.put(
            f'/api/v1/board/{self.category.id}/post/{self.post.id}/comment/{self.comment.id}/reply/{self.reply.id}', 
            json.dumps(context), **self.header, content_type='application/json')
        self.assertEqual(response.status_code, 201)
    
    
    def test_like_reply(self):
        response = self.client.post(
            f'/api/v1/board/{self.category.id}/post/{self.post.id}/comment/{self.comment.id}/reply/{self.reply.id}', 
            **self.header, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        
        
    def test_delete_reply(self):
        response = self.client.delete(
            f'/api/v1/board/{self.category.id}/post/{self.post.id}/comment/{self.comment.id}/reply/{self.reply.id}', 
            **self.header, content_type='application/json')
        self.assertEqual(response.status_code, 204)
        
        self.reply.delete()
    
    
    def test_modify_comment(self):
        context = {
            'content': "수정된 댓글",
        }
        
        response = self.client.put(
            f'/api/v1/board/{self.category.id}/post/{self.post.id}/comment/{self.comment.id}', 
            json.dumps(context), **self.header, content_type='application/json')
        self.assertEqual(response.status_code, 201)
    
    
    def test_like_comment(self):
        response = self.client.post(
            f'/api/v1/board/{self.category.id}/post/{self.post.id}/comment/{self.comment.id}', 
            **self.header, content_type='application/json')
        self.assertEqual(response.status_code, 200)
    
    
    def test_delete_comment(self):
        response = self.client.delete(
            f'/api/v1/board/{self.category.id}/post/{self.post.id}/comment/{self.comment.id}', 
            **self.header, content_type='application/json')
        self.assertEqual(response.status_code, 204)
        
        self.comment.delete()
    