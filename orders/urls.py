from django.urls import path
from .views import create_order
# представление create_order из views

# заказы
app_name = 'orders'
urlpatterns = [
    path('new_order/', create_order, name='order_create'),
    
]