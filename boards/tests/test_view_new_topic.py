from django.test import TestCase
from django.urls import reverse, resolve
from boards.models import Board

class LoginRequiredNewTopicTest(TestCase):
	def setUp(self):
		self.url = reverse('new_topic', kwargs = {'pk':1})
		Board.objects.create(name="Dave", description="It's very difficult")

	def redirectTest(self):
		response = self.client.get(self.url)
		login_url = reverse('login')
		self.redirectTest(response, '{login_url}?next={url}'.format(login_url=login_url, url=self.url))

	def invalidDataTest(self):
		response = self.client.post(self.url, {})
		form = response.context.get('form')
		self.assertTrue(form.errors)
