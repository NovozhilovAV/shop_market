from django.urls import path
from .views import index
# маршрутизатор приложения products

app_name = 'products'
urlpatterns = [
    path('', index, name='index'),
    # path('product-list/', index, name='index'),

]
