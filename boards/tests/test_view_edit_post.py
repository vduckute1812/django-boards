from django.test import TestCase
from django.urls import reverse, resolve
from django.utils import timezone
from boards.models import Board, Topic, Post
from django.contrib.auth.models import User

class PostUpdateViewTestCase(TestCase):
	def setUp(self):
		self.board = Board.objects.create(name='Test', description='No more')
		self.username = 'vanducprocf113'
		self.password = 'vanduc1812'
		self.user = User.objects.create_user(username=self.username, password = self.password,  email='jane@doe.com')
		self.topic = Topic.objects.create(starter= self.user, subject= 'Nothing here', board=self.board, last_updated=timezone.now())
		self.post = Post.objects.create(message='Please come back', topic=self.topic, created_at=timezone.now(), created_by=self.user)
		self.url = reverse('edit_post', kwargs={'pk':self.board.pk, 'topic_pk':self.topic.pk, 'post_pk':self.post.pk})
	def get_queryset(self):
		queryset = super().get_queryset()
		return queryset.filter(created_by=self.request.user)

	def form_valid(self, form):
		post = form.save(commit=False)
		post.updated_by = self.request.user
		post.updated_at = timezone.now()
		post.save()
		return redirect('topic_posts', pk=post.topic.board.pk, topic_pk=post.topic.pk)

class LoginRequiredPostUpdateViewTests(PostUpdateViewTestCase):
	def test_redirection(self):
		'''
		Test if only logged in user can edit the post
		'''
		login_url = reverse('login')
		response = self.client.get(self.url)
		self.assertRedirects(response, '{login_url}?next={url}'.format(login_url=login_url, url = self.url))

class UnauthorizedPostUpdateViewTest(PostUpdateViewTestCase):
	'''
	Create new User different from new one posted
	'''
	def setUp(self):
		super().setUp()
		username = 'jane'
		password = '321'
		user = User.objects.create_user(username=username, email='jane@doe.com', password=password)
		self.client.login(username=username, password=password)
		self.response = self.client.get(self.url)
		print(self.response)


	def test_status_code(self):
		self.assertEquals(self.response.status_code, 404)

