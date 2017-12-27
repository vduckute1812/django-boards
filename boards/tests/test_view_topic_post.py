from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse

from ..models import Board, Post, Topic
from ..views import topic_posts, PostListView


class TopicPostsTests(TestCase):
    def setUp(self):
        board = Board.objects.create(name='Django2', description='Django board2.')
        user = User.objects.create_user(username='john21sad23asd', email='john2@doe.com', password='123as2d123')
        topic = Topic.objects.create(subject='Hello, world 123', board=board, starter=user)
        Post.objects.create(message='Lorem ipsum dolor2 sit amet', topic=topic, created_by=user)
        url = reverse('topic_posts', kwargs={'pk': board.pk, 'topic_pk': topic.pk})
        self.response = self.client.get(url)
        self.topic = Topic.objects.get(subject='Hello, world 123')


    def test_status_code(self):
        if(self.topic.posts.count()!=0):
            self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/boards/1/topics/1/')
        self.assertEquals(view.func.view_class, PostListView)
