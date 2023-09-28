from django.urls import path
from .views import create_order OrdersListView, 
# представление create_order из views

# заказы
app_name = 'orders'
urlpatterns = [
    path('', OrdersListView.as_view(), name='order-list'),
    path('new_order/', create_order, name='order_create'),
    # path('order-info/<str:pk>/', OrderDetailView.as_view(), name='order-detail'),
    
]