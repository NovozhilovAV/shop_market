from typing import Any, Dict
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import CreateView, ListView, DetailView
from .models import Category, Subcategory, Products
from .forms import CategoryForm, SubcategoryForm, ProductForm
from django.urls import reverse_lazy
from django import template


register = template.Library()
# wtf???

# # так было в начале,тренировались
# def index(request):
#     return HttpResponse('This is page Products/это страница c продуктами!')

# def root_index(request):
#     # return render(request, 'products/base.html')
#     # выедет меню из base.html
#     return render(request, 'products/index.html')
#     # выведет страницу index.html с приветствием и стилем stylesheet

def index(request):
    category = Category.objects.all()
    context = {
        'category_list': category
    }
    return render(request, 'products/index.html', context=context)

class CategoryCreateView(CreateView):
    model = Category
    fields = '__all__'
    form = CategoryForm
    template_name = 'products/category_form.html'
    success_url = reverse_lazy('products:category_list')


class CategoryListView(ListView):
    model = Category
    template_name = 'products/category_list.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        subcategories = Subcategory.objects.all()
        context['subcategories'] = subcategories
        return context


class SubCategoryCreateView(CreateView):
    model = Subcategory
    fields = '__all__'
    form = SubcategoryForm
    template_name = 'products/subcategory_form.html'
    success_url = reverse_lazy('products:category_list')


# представление создания продукта
class ProductCreateView(CreateView):
    model = Products
    fields = '__all__'
    form = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('products:index')

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['subcategories'] = Subcategory.objects.all()
        return context

    def form_valid(self, form):
        self.instance = form.save(commit=False)
        self.instance.category_id = self.request.POST.get('category')
        self.instance.subcategory_id = self.request.POST.get('subcategory')
        self.instance.save()
        return super().form_valid(form)


class ProductListView(ListView):
    model = Products
    template_name = 'products/product_list.html'
    context_object_name = 'products'


    def get_queryset(self):
        super().get_queryset()    # родительский класс
        slug = self.request.resolver_match.kwargs['subcat_slug']    # получаем ключ сабкатегории
        queryset = Products.objects.filter(subcategory__slug = slug) # фильтруем продукты через подкатегорию по слагу
        # подчеркивание двойное - связь с полем модели 
        return queryset
    
    # переопределили контекст чтобы туда поподала форма
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        cart_product_form = ()
        # форма добавления продукта
        context['cart_product_form'] = cart_product_form
        return context
    
    # карточка товара
class ProductDetailView(DetailView):
    model = Products
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'prod_slug'
    
    

# def CategoryDetail(request, category_slug):
#     category = get_object_or_404(Category, slug=category_slug)
#     subcategory = Subcategory.objects.filter(category=category)
#     context = {
#         'category': category,
#         'subcategory': subcategory
#     }
#     return render(request, 'products/category_detail.html', context=context)    
