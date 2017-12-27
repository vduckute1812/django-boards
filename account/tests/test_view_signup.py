from django.test import TestCase
from django.urls import reverse, resolve
from ..views import signup
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import User
from account.forms import SignUpForm
# Create your tests here.
class SignUpTest(TestCase):
	def setUp(self):
		url = reverse('signup')
		self.response = self.client.get(url)

	def test_view_signup_status_code(self):
		self.assertEqual(self.response.status_code, 200)

	def test_view_resolve_test_url(self):
		view = resolve('/signup')
		self.assertEqual(view.func, signup)

	def test_new_signup_add_valid_post_data(self):
		url = reverse('signup')
		response = self.client.post(url, {})
		self.assertEquals(response.status_code, 200)

	def test_crfs(self):
	    self.assertContains(self.response, 'csrfmiddlewaretoken')
	
	def test_contains_form(self):
		form = self.response.context.get('form')
		self.assertIsInstance(form, SignUpForm)

	def test_form_inputs(self):
		self.assertContains(self.response,'<input', 5)
		self.assertContains(self.response, 'type="text"', 1)
		self.assertContains(self.response, 'type="email"', 1)
		self.assertContains(self.response, 'type="password"', 2)

class SignUpSuccessFull(TestCase):
	def setUp(self):
		url = reverse('signup')
		data = {
		'username' : "ducbkdn123",
		'email'    : "ducbkdn95@gmail.com",
		'password1' : "nothing123",
		'password2' : "nothing123"
		}
		self.response = self.client.post(url, data)
		self.url_home = reverse('home')

	def test_redirect_to_home(self):
		self.assertRedirects(self.response, self.url_home)

	def test_User_creation(self):
		self.assertTrue(User.objects.exists())

	def test_user_authenticate(self):
		response = self.client.get(self.url_home)
		user = response.context.get('user')
		self.assertTrue(user.is_authenticated)

class SignUpUnSuccessFull(TestCase):
	def setUp(self):
		url = reverse('signup')
		self.response = self.client.post(url, {})
		self.url_home = reverse('home')


	def test_Invalid_Data(self):
		self.assertEquals(self.response.status_code, 200)

	def test_form_error(self):
		form = self.response.context.get('form')
		self.assertTrue(form.errors)