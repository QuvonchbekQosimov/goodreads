from django import forms
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


class CustomUserCreateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email']


class CustomUserLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        user = CustomUser.objects.filter(username=username).first()
        if not user or not user.check_password(password):
            raise forms.ValidationError('Invalid username or password')
        return cleaned_data

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = CustomUser.objects.filter(username=username).first()
        if user and user.check_password(password):
            return user
        return None


class CustomUserLogoutForm(forms.Form):
    pass
