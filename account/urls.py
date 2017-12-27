from django.urls import path, include, re_path
from account import views

urlpatterns = [
	path('', views.signup, name='signup'),
	]
