from django import forms
# подключили библитеку с формами
from .models import Category, Subcategory, Products
# импоритруем модели


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        # exclude = исключаем поля которые не хотим отображать
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
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    subcategory = forms.ModelChoiceField(queryset=Subcategory.objects.all())
    
    class Meta:
        model = Products
        exclude = ['created_at', 'is_availabel']
        # исключения 