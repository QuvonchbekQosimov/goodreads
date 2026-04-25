from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views import View
from httplib2 import Authentication

from users.forms import UserCreateForm


class RegisterView(View):
    def get(self, request):
        create_form = UserCreateForm()
        context = {
            'form': create_form
        }
        return render(request, 'users/register.html', context)

    def post(self, request):

        create_form = Authentication(data=request.POST)

        if create_form.is_valid():
            create_form.save()
            return redirect('users:login')
        else:
            context = {
                'form': create_form
            }
            return render(request, 'users/register.html', context)


class LoginView(View):
    def get(self, request):
        login_form = Authentication()
        return render(request, 'users/login.html', {'form': login_form})

    def post(self, request):
        login_form = Authentication(data=request.POST)

        if login_form.is_valid():
            user = login_form.login(request)
            if user:
                login(request, user)
                return redirect('landing_page')
        return render(request, 'users/login.html', {'form': login_form})
