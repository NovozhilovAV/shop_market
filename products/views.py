from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import CreateView
from .models import Category, Subcategory,Products
from .forms import CategoryForm, SubcategoryForm, ProductForms


# Create your views here.
def index(request):
    return HttpResponse('This is page Products')

def root_index(request):
    return render(request, 'products/base.html')

class CategoriCreateView(CreateView):
    models = Category