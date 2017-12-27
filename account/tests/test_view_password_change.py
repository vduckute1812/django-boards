from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

class PasswordChangeTestCase(TestCase):
    def setUp(self, data={}):
        self.user = User.objects.create_user(username='john', email='john@doe.com', password='old_password')
        self.url = reverse('password_change')
        self.client.login(username='john', password='old_password')
        self.response = self.client.post(self.url, data)

        
class LoginRequiredPasswordChangeTest(TestCase):

	def test_redirect_change_password(self):
		login_url = reverse('login')
		url = reverse('password_change')
		response = self.client.get(url)
		self.assertRedirects(response, f'{login_url}?next={url}')

class SuccessfulPassWordChangeTest(PasswordChangeTestCase):
	def setUp(self):
		super().setUp({
			'old_password':'old_password',
			'new_password1':'new_password',
			'new_password2':'new_password'	
		})

	def test_redirect(self):
		self.assertRedirects(self.response, reverse('password_change_done'))

	def test_password_changed(self):
		self.user.refresh_from_db()
		self.assertTrue(self.user.check_password('new_password'))

	def test_user_authenticated(self):
		response = self.client.get(reverse('home'))
		user = response.context.get('user')
		self.assertTrue(user.is_authenticated)


class InvalidPassWordChangeTest(PasswordChangeTestCase):
	def setUp(self):
		super().setUp({
			'old_password':'old_password',
			'new_password1':'new_password',
			'new_password2':'wrong_password'
			})

	def test_status_code(self):
		self.assertEquals(self.response.status_code, 200)

	def test_unchange_password(self):
		self.user.refresh_from_db()
		self.assertTrue(self.user.check_password('old_password'))

	def test_form_error(self):
		form = self.response.context.get('form')
		self.assertTrue(form.errors)