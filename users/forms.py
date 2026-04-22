from django import forms
from django.contrib.auth.models import User


class UserCreateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data['username']
        password = cleaned_data['password']
        user = User.objects.filter(username=username).first()
        if not user or not user.check_password(password):
            raise forms.ValidationError('Invalid username or password')
        return cleaned_data

    def login(self, request):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = User.objects.filter(username=username).first()
        if user and user.check_password(password):
            return user
        return None


class UserLogoutForm(forms.Form):
    pass
