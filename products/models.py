from django.db import models
from django.urls import reverse
from slugify import slugify


# Create your models here. добавляем модели
class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Имя категории', unique=True)
    description = models.TextField(max_length=1000, verbose_name='Описание категории')
    slug = models.SlugField(max_length=70, unique=True, verbose_name='URL-имя', editable=False)  # отоброжает имя сущности

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name',]

    def __str__(self) -> str:
        return self.name
    
    def get_url(self):    # используется для получения URL возвращает страниц
        return reverse('category_detail', args=[self.slug])
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)
    


class Subcategory(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Имя подкатегории')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Категория', related_name='category' )
    # category = models.ForeignKey(to='Category') - так тоже можно написать
    slug = models.SlugField(max_length=70, unique=True, verbose_name='URL-имя', editable=False)  # отоброжает имя сущности

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'
        ordering = ['name',]

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Subcategory, self).save(*args, **kwargs)


class Products(models.Model):
    name = models.CharField(max_length=128, unique=True, verbose_name='Имя товара')
    description = models.TextField(max_length=1000, verbose_name='Описание товара')
    price = models.FloatField(verbose_name='Цена товара')
    slug = models.SlugField(max_length=140, unique=True, verbose_name='URL-имя')
    is_available = models.BooleanField(default=True, verbose_name='Доступность товара')
    created_at = models.DateField(auto_now_add= True, verbose_name='Дата добавления товара')
    image = models.ImageField(upload_to='images/', verbose_name='Изображение товара')
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, verbose_name='Подкатегории')
    slug = models.SlugField(max_length=70, unique=True, verbose_name='URL-имя', editable=False)  # отоброжает имя сущности

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['name', '-price']

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])
    
    def __str__(self) -> str:
        return self.name
    


# Category
# Subcategory
# product