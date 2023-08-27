from django.urls import path
from .views import index, CategoryCreateView, CategoryListView
# маршрутизатор приложения products
# видео от 24.08 - 2ч35мин

app_name = 'products'
urlpatterns = [
    path('', index, name='index'),
    path('category_form/', CategoryCreateView.as_view(), name='category_form'),
    path('category_list/', CategoryListView.as_view(), name='category_list'),

]
