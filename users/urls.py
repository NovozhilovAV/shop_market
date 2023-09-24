from django.urls import path
<<<<<<< HEAD
# from .views import register.....
from .views import *
=======
from .views import register, log_out, log_in
>>>>>>> 68da62b (refresh project 22/09/23)

app_name = 'users'
urlpatterns = [
    path('register/', register, name='register'),
    path('login/', log_in, name='login'),
    path('logout/', log_out, name='logout'),
    
]
