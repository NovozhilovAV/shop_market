from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import CreateView, ListView
from .models import Category, Subcategory, Products
from .forms import CategoryForm, SubcategoryForm, ProductForm
from django.urls import reverse_lazy


# Create your views here.
def index(request):
    return HttpResponse('This is page Products')

def root_index(request):
    return render(request, 'products/base.html')
    # выедет меню из base.html
    # return render(request, 'products/index.html')
    # выведет страницу index.html с приветствием и стилем stylesheet

class CategoryCreateView(CreateView):
    models = Category
    fields = '__all__'
    form = CategoryForm
    template_name = 'products/category_form.html'
    success_url = reverse_lazy('products:category_list')


class CategoryListView(ListView):
    model = Category
    template_name = 'products:category_list.html'
    context_object_name = 'categories'