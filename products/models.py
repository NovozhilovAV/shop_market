from django.db import models
from django.urls import reverse
from slugify import slugify
import os



def create_directory_path(instance):
    return os.path.join('images', instance.category.slug, instance.subcategory.slug)
    # return f'images/{instance.category.slug}/{instance.subcategory.slug}'
# добавление директории с изображениями

# Create your models here. добавляем модели
class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Имя категории', unique=True)
    description = models.TextField(max_length=1000, verbose_name='Описание категории')
    slug = models.SlugField(max_length=256, unique=True, verbose_name='URL-имя', editable=False)  

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name',]

    def __str__(self) -> str:
        return self.name
    
    # используется для получения URL возвращает страницу
    def get_url(self):    
        return reverse('category_detail', args=[self.slug])
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)
  

class Subcategory(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Имя подкатегории')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Категория', related_name='categories' )
    slug = models.SlugField(max_length=70, unique=True, verbose_name='URL-имя', editable=False)  # отоброжает имя сущности

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'
        ordering = ['name',]

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Subcategory, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name
    
    # Используется для получения URL возвращает страничку
    def get_absolute_url(self):  
        return reverse('products:product_list', kwargs={'cat_slug': self.category.slug, 'subcat_slug':self.slug}) 


class Products(models.Model):
    name = models.CharField(max_length=128, unique=True, verbose_name='Название товара')
    description = models.TextField(max_length=1000, verbose_name='Описание товара')
    price = models.FloatField(verbose_name='Цена товара')
    slug = models.SlugField(max_length=148, unique=True, verbose_name='URL-имя', editable=False)
    is_available = models.BooleanField(default=True, verbose_name='Доступность товара')
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата добавления товара')
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, verbose_name='Подкатегория', editable=False, related_name='subcategory')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория', editable=False, related_name='category')
    image = models.ImageField(upload_to=create_directory_path, verbose_name='Изображение товара', null=True, blank=True)


    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['name', '-price']

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])
    
    def __str__(self) -> str:
        return self.name
    
    # Используется для получения URL возвращает страничку
    def get_absolute_url(self):    
        return reverse('products:product_detail', kwargs={
            'cat_slug': self.category.slug, 
            'subcat_slug':self.slug,
            'prod_slug': self.slug            
            }
        ) 
    
    # формирует слаг
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Products, self).save(*args, **kwargs)


# Category
# Subcategory
# product