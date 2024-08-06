from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import MyUser


class RegisterUserForm(UserCreationForm):

    class Meta:
        model = MyUser
        fields = (
            'phone_number',
            'first_name'
        )


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(
        label="Номер телефона",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )



