from django import forms
# подключили библитеку с формами
from .models import Category, Subcategory, Products
# импоритруем модели


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        labels = {
            'name': 'Имя',
            'description': 'Описание',
            'slug': 'URL-адрес',
        }


class SubcategoryForm(forms.ModelForm):
    class Meta:
        model = Subcategory
        fields = '__all__'
        # все поля в модели должны быть использованны
        labels = {
            'name': 'Подкатегория',
            'category': 'Категория',
        }
        # устанавливает текстовую метку рядом с полем
        

class ProductForm(forms.ModelForm):
    class Meta:
        model = Products
        exclude = ['created_at', 'is_availabel']
        # исключения 