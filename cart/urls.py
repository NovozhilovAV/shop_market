from django.urls import path
# from .views import cart_add, cart_detail, cart_remove
from .views import *


app_name = 'cart'
urlpatterns = [
    path('', cart_detail, name='cart_detail'),
    # 
    path('add/<int:product_id>/', cart_add, name='cart-add'),
    path('remove/<int:product_id>/', cart_remove, name='cart-remove'),
    
]