from django.urls import resolve, reverse, Resolver404
from django.test import TestCase
from ..views import home, board_topics, new_topic, BoardListView, TopicListView
from boards.models import Board, Topic, Post
from boards.forms import NewTopicForm
from django.contrib.auth.models import User


class HomeTests(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Python-Django', description=' I will change the world')
        url = reverse('home')
        self.response = self.client.get(url)

    def test_home_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func.view_class, BoardListView)

    def test_home_view_contains_link_to_topics_page(self):
        board_topics_url = reverse('board_topics', kwargs={'pk': self.board.pk})
        self.assertContains(self.response, 'href="{0}"'.format(board_topics_url))


class BoardTopicsTests(TestCase):

    def setUp(self):
        Board.objects.create(name='Django', description='Django board.')

    def test_board_topics_view_success_status_code(self):
        url = reverse('board_topics', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_board_topics_view_not_found_status_code(self):
        url = reverse('board_topics', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_board_topics_url_resolves_board_topics_view(self):
        view = resolve('/boards/page-8/')
        self.assertEquals(view.func.view_class, TopicListView)

    def test_board_topics_view_contains_link_back_to_homepage(self):
        board_topics_url = reverse('board_topics', kwargs={'pk': 1})
        homepage_url = reverse('home')
        response = self.client.get(board_topics_url)
        self.assertContains(response, 'href="{0}"'.format(homepage_url))

    def test_user_profile_status_code(self):
        url = reverse('user_profile', kwargs={'username': 'asdkgh@ask'})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)


class CreateNewTopic(TestCase):
    def setUp(self):
        Board.objects.create(name='Django', description='Django board.')
        User.objects.create_user(username='vduc12345', email='ducbkdn95@gmail.com', password='asdas12431')
        self.client.login(username='vduc12345', password='asdas12431')

    def test_new_topic_view_success_status_code(self):
        url = reverse('new_topic', kwargs = {'pk' : 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_new_topic_view_not_found_status_code(self):
        url = reverse('new_topic', kwargs = {'pk' : 99})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_new_topic_url_resolves_new_topic_view(self):
        view = resolve('/boards/1/new/')
        self.assertEquals(view.func, new_topic)

    def test_new_topic_view_containt_link_back_to_home(self):
        new_topic_url = reverse('new_topic', kwargs = {'pk' : 1})
        response = self.client.get(new_topic_url)
        homepage_url = reverse('home')        
        self.assertContains(response, 'href="{0}"'.format(homepage_url))

    def test_new_topic_view_resolves_new_topic_url(self):
        url = reverse('new_topic', kwargs = {'pk':1})
        

    def test_new_topic_view_contains_link_back_to_board_topics_view(self):
        new_topic_url = reverse('new_topic', kwargs={'pk': 1})
        board_topics_url = reverse('board_topics', kwargs={'pk': 1})
        response = self.client.get(new_topic_url)
        self.assertContains(response, 'href="{0}"'.format(board_topics_url))

    def test_board_topic_contains__negative_link(self):
        new_topic_url = reverse('new_topic', kwargs = {'pk':1})
        board_topics_url = reverse('board_topics', kwargs={'pk': 1})
        homepage_url = reverse('home')        
        response = self.client.get(board_topics_url)
        self.assertContains(response, 'href="{0}"'.format(homepage_url))        
        self.assertContains(response, 'href="{0}"'.format(new_topic_url))

    def test_csrf_token(self):
        url = reverse('new_topic', kwargs={'pk':1})
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_new_topic_view_add_valid_data(self):
        url = reverse('new_topic', kwargs={'pk':1})
        data = {
        'subject': 'Test',
        'message': "It's good"
        }
        response = self.client.post(url, data)
        self.assertTrue(Topic.objects.exists())
        self.assertTrue(Post.objects.exists())

    def test_new_topic_new_add_invalid_post_data(self):
        url = reverse('new_topic', kwargs={'pk':1})
        response = self.client.post(url,{})
        self.assertEquals(response.status_code, 200)

    def test_new_topic_add_invalid_data(self):
        url = reverse('new_topic',kwargs = {'pk':1})
        data = {
        'subject': '',
        'message': ''
        }
        response = self.client.post(url, data)
        self.assertFalse(Post.objects.exists())
        self.assertFalse(Topic.objects.exists())
        self.assertEquals(response.status_code, 200)

    def test_contants_form(self):
        url = reverse('new_topic', kwargs={'pk':1})
        response = self.client.get(url)
        form = response.context.get('form')
        self.assertIsInstance(form, NewTopicForm)

    def test_form_with_invalid_data(self):
        url = reverse('new_topic', kwargs={'pk':1})
        response = self.client.post(url,{})
        form = response.context.get('form')
        self.assertTrue(form.errors)
        self.assertEqual(response.status_code, 200)
