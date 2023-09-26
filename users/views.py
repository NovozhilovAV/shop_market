from django.shortcuts import redirect, render
from .forms import UserRegistrationForm
# from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from int_shop.settings import LOGIN_REDIRECT_URL
from .forms import AuthForm
from django.views.generic import DetailView
from django.contrib.auth.models import User


# Видео о 6.07.23 8 минута
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)    # то,что берется из запроса
        if user_form.is_valid():
            # Добавляем нового пользователя и сохроняем 
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            return render(request, 'users/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'users/register.html', {'user_form': user_form})
    # при успешной регистрации перейдем на этот адрес
# так внутри создается пользователь - создается запись во встроенной таблице User
# user = User.objects.create_user("john", "lennon@thebeatles.com", "johnpassword")


def log_in(request):
    # form = AuthenticationForm(request, data=request.POST or None)
    form = AuthForm(request, data=request.POST or None)


    if form.is_valid():     # если форма валидна(корректная)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            # url = reverse('products:index')
            url = request.GET.get('next', LOGIN_REDIRECT_URL)   # внизу в settings.py
            return redirect(url)
    #     1 видео от 6.07 53 минута

    return render(request, 'users/login.html', {'form': form})


def log_out(request):
    logout(request)
    url = reverse('products:index')
    return redirect(url)


class UserDetailView(DetailView):
    # определили класс(наследуем его) - отображение страницы пользователя
    model = User    # модель - Юзер - берет данные
    template_name = 'user/user_info.html'
    # Имя шаблона куда выводится - где отрисовывается