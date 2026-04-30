from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View

from users.forms import CustomUserCreateForm, CustomUserUpdateForm


class RegisterView(View):
    def get(self, request):
        create_form = CustomUserCreateForm()
        context = {
            'form': create_form
        }
        return render(request, 'users/register.html', context)

    def post(self, request):

        create_form = CustomUserCreateForm(data=request.POST)

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
        login_form = AuthenticationForm(data=request.POST)

        if login_form.is_valid():
            user = login_form.get_user()
            if user:
                login(request, user)
                messages.success(request, "Login successful")
                return redirect('books:list')

        return render(request, 'users/login.html', {'form': login_form})


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'users/profile.html', {'user': request.user})


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.info(request, "Logout successful")
        return redirect('landing_page')


class ProfileUpdateView(LoginRequiredMixin, View):
    def get(self, request):
        user_update_form = CustomUserUpdateForm(instance=request.user)
        return render(request, 'users/profile_edit.html', {'form': user_update_form})

    def post(self, request):
        user_update_form = CustomUserUpdateForm(instance=request.user, data=request.POST)
        if user_update_form.is_valid():
            user_update_form.save()
            messages.success(request, "You have successfully updates your profile.")
            return redirect('users:profile')
        return render(request, 'users/profile_edit.html', {'form': user_update_form})
