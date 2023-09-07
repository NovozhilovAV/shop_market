from django.urls import path
from .views import *
# from .views import index, CategoryCreateView, CategoryListView, SubCategoryCreateView
# маршрутизатор приложения products
# видео от 24.08 - 2ч35мин

app_name = 'products'
urlpatterns = [
    path('', index, name='index'),

    path('category_form/', CategoryCreateView.as_view(), name='category_form'),
    path('category_list/', CategoryListView.as_view(), name='category_list'),
    path('subcategory_form/', SubCategoryCreateView.as_view(), name='subcategory_form'),

    path('product_form/', ProductCreateView.as_view(), name='product_form'),
    path('product_list/<slug:cat_slug>/<slug:subcat_slug>/', ProductListView.as_view(), name='product_list'),
    path('product-detail/<slug:cat_slug>/<slug:subcat_slug>/<slug:prod_slug>/', ProductDetailView.as_view(), name='product_detail'),

    path('product_form/', ProductCreateView.as_view(), name='product_form'),
    path('product_list/<slug:cat_slug>/<slug:subcat_slug>/', ProductListView.as_view(), name='product_list'),
    path('product_detail/<slug:cat_slug>/<slug:subcat_slug>/<slug:prod_slug>/', ProductDetailView.as_view(), name='product_detail'),
]
