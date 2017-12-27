from django.shortcuts import render, redirect
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from account.forms import SignUpForm
from django.contrib import auth

# Create your views here.
def signup(request):
    if(request.user.is_authenticated):
        return redirect('home')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})



"""To log a user in, from a view, use login(). It takes an 
HttpRequest object and a User object. login() saves the user’s ID 
in the session, using Django’s session framework."""

