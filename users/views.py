from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.http import HttpResponse




class RegisterView(View):
    def get(self, request):
        return render(request, 'users/register.html')
    def post(self, request):
        user = User.objects.create_user(
            username=request.POST['username'],
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email']
        )
        user.set_password(request.POST['password'])
        user.save()
        return redirect('users:login')

class LoginView(View):
    def get(self, request):
        return render(request, 'users/login.html')