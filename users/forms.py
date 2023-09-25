from django.contrib.auth.models import User
# стандартная модель джанго в модуле аунтефикации
from django.utils.translation import gettext_lazy as _
from django import forms  ## Для переопределения полей в формах
from django.contrib.auth.forms import AuthenticationForm, UsernameField


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput,
                               error_messages={'required': 'Плиз, заполните поле!'})
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')    # выбрали поля из модели
        help_texts = {
            'username': 'Только буквы, цифры и символы @/./+/-/_',
        }
        # переназвали поля по русски
        labels = {
            'username' : 'Логин',
            'first_name' : 'Имя пользователя',
            'email' : 'почта'
        }

    def clean_password2(self):  ## Важно чтобы начиналось со слова clean_<имя поля>
        cd = self.cleaned_data  ## В момент валидации создается словарик
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают!')  ## raise в "ручном" режиме генерирует исключение
        return cd['password2']
    
class AuthForm(AuthenticationForm):
    username = UsernameField(
        widget=forms.TextInput(attrs={"autofocus": True}),
        label=_("Логин"),
    )
    # username = UsernameField(
        # widgets = {
        #     'username': forms.TextInput,
        #     'email': forms.EmailInput,
        #     'first_name': forms.TextInput,
        # }.TextInput(attrs={"autofocus": True}),
        # label=_("Логин"),
    # )
    password = forms.CharField(
        label=_("Пароль"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )

    error_messages = {
        "invalid_login": _(
            "Введите коректные логин и пароль. Внимание! "
            "Поля могут быть чувствительны к регистру."
        ),
        "inactive": _("Этот аккаунт заблокирован."),
    }


#    class AuthForm(AuthenticationForm):
#     username = UsernameField(
#         widget=forms.TextInput(attrs={"autofocus": True}),
#         label=_("Логин"),
#     )
#     password = forms.CharField(
#         label=_("Пароль"),
#         strip=False,
#         widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
#     )
#     error_messages = {
#         "invalid_login": _(
#             "Пожалуйста введите коректные логин и пароль. Обратите внимание на то, что! "
#             "поля могут быть чувствительны к регистру."
#         ),
#         "inactive": _("Этот аккаунт заблокирован."),
#     }