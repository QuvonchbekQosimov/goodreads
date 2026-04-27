from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.views import View

from users.forms import UserCreateForm


class RegisterView(View):
    def get(self, request):
        create_form = UserCreateForm()
        context = {
            'form': create_form
        }
        return render(request, 'users/register.html', context)

    def post(self, request):

        create_form = UserCreateForm(data=request.POST)

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
        login_form = AuthenticationForm()
        return render(request, 'users/login.html', {'form': login_form})

    def post(self, request):
        # 1-TUZATISH: UserCreateForm o'rniga AuthenticationForm yozamiz
        login_form = AuthenticationForm(data=request.POST)

        if login_form.is_valid():
            # 2-TUZATISH: .login() emas, .get_user() orqali foydalanuvchini olamiz
            user = login_form.get_user()
            if user:
                login(request, user)
                return redirect('landing_page')

        return render(request, 'users/login.html', {'form': login_form})


class ProfileView(View):
    def get(self, request):
        return render(request, 'users/profile.html', {'user': request.user})
