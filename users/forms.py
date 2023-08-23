from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django import forms


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput,
                               error_messages={'required': 'Плиз, заполните поле!'})
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')
        help_texts = {
            'username': 'Только буквы, цифры и символы @/./+/-/_',
        }
        labels = {
            'username' : 'Логин',
            'first_name' : 'Имя пользователя',
            'email' : 'почта'
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают!')
        return cd['password2']