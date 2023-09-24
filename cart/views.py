from int_shop import settings
from products.models import Products
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from products.models import Products
from .forms import CartAddProductForm
from cart.models import CartItem, CartUser

# создаем класс корзины. она связана с сесией

class Cart:
    def __init__(self, request):
        # получили сессию
        self.session = request.session
        # из нашей сессии получили id сессии
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
            # если сессии не было то создадим пустую корзину и присвоим пустой словарь 
        
        self.cart = cart
        # принимает корзину из сесии - 

        # метод-добавить и аргументы - корзина, продукты, количество...
    def add(self, product, quantity=1, override_quantity=False):
        product_id = str(product.id)
        # получаем id товара - в виде строки 
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)
            }
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    # сохранение
    def save(self):
        self.session.modified = True
    
    # удаление товара (сессии из словаря)
    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    # условия итерации - при прохожденни циклом в корзине
    def __iter__(self):
        # получаем все ключи
        product_ids = self.cart.keys()
        # фильтруем по id продукта
        products = Products.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        # связываем id продукта с самим продуктом
        for product in products:
            cart[str(product.id)]['product'] = product
        
        for item in cart.values():
            # значение цены
            item['price'] = Decimal(item['price'])
            # итоговая цена с количеством
            item['total_price'] = item['price'] * item['quantity']
            yield item
       
    # учим считать корзину
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
    
    # итоговая стоимость 
    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())  
    
    # очистка корзины - удаление из сесии
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

# только для пост запроса 
@require_POST
def cart_add(request, product_id):
    # создаем объект корзины или получаем из сессии
    if request.user.id:
        return add_cart_db(request, product_id)
    cart = Cart(request)
    # если пользователь авторизирован то добавляем
    # в БД товар ....
     
    # создаем товар
    product = get_object_or_404(Products, id=product_id)
    form = CartAddProductForm(request.POST)
    # форма для количества товара
    
    if form.is_valid():
        # если данные корректны то создаем пееременную
        cd = form.cleaned_data
        # добавление продукт - количество - перезаписывать?да-нет
        cart.add(product=product, 
                 quantity=cd['quantity'],
                 override_quantity=cd['override'])
    else:
        cart.add(product=product, 
                 quantity=1,
                 override_quantity=False)
    
    return redirect('cart:cart__detail')
    # перенапправляем на страниу корзины

@require_POST
def cart_remove(request, product_id):
    if request.user.id:
        return remove_from_db(request, product_id)
    # еслю пользователь зарегистрирован и удаляет товар 
    # то товар удаляется из БД

    cart = Cart(request)
    product = get_object_or_404(Products, id=product_id)
    cart.remove(product)
    
    return redirect('cart:cart-detail')


def cart_detail(request):
    if request.user.id:
        cart = ProductCartUser(request)
    else:
        cart = Cart(request)

    cart = Cart(request)
    for item in cart:
        # для каждой позиции добавляем форму со значениями
        item['update_quantity_form'] = CartAddProductForm(initial={
            # количество из элемента "количество" в форме
            'quantity': item['quantity'],
            # перезаписываем  значение 
            'override': True})
    return render(request, 'cart/cart-detail.html', {'cart': cart})
    # вывели страницу 

# корзина для авторизованного пользователя (хранится постоянно  в БД)
class ProductCartUser:
    # инициализация корзины
    def _init_(self, request):
        # создаем объект словаря для хранения товаров
        self.cart = {}
        # получаем текущего пользователя, чтобы знать, с чьей корзиной работать
        self.user = request.user
        # получаем корзину пользователя из БД или создаем пустую (если нет корзины)
        self.user_cart, created = CartUser.objects.get_or_create(user=self.user)
        # получаем позиции товаров в корзине
        products_in_cart = CartItem.objects.filter(cart=self.user_cart)
        """ заполняем корзину (словарь) элементами из корзины (БД) 
        {
        "1": 
          {
           "quantity": "2",
           "price": "35000.00"
          },
          "2": 
          {
           "quantity": "3",
           "price": "40000.00"
          },
        }
        """
        for item in products_in_cart:
            self.cart[str(item.product_id)] = {'quantity': str(item.quantity), 'price': str(item.product.price)}
 
    # метод добавления товара в корзину (словарь)
    def add(self, product, quantity=1, override_quantity=False):
        product_id = str(product.id)
        #product = Products.objects.get(pk=product.id)
 
        # проверяем наличие товара в корзине, если нет, то добавляем товар
        if product_id not in self.cart:
            self.cart[product_id]={'quantity': str(quantity), 'price': str(product.price)}
        # иначе - обновляем количество
        else:
            # если не нужно перезаписать количество
            if not override_quantity:
                # увеличиваем количество товара на необходимое
                current_quantity = int(self.cart[product_id]['quantity'])
                self.cart[product_id]['quantity'] = str(current_quantity+quantity)
            # иначе - перезаписываем
            else:
                self.cart[product_id]['quantity'] = quantity
        # вызываем метод сохранения в БД
        self.save()
 
    # метод сохранения в БД
    def save(self):
        # получаем каждый продукт по его ИД в словаре
        for id in self.cart:
            product = Products.objects.get(pk=int(id))
            # проверяем наличие товара в корзине БД
            # если есть - обновляем количество товара            
            if CartItem.objects.filter(cart=self.user_cart, product=product).exists():
                item = CartItem.objects.get(cart=self.user_cart, product=product)
                item.quantity = self.cart[id]['quantity']
                item.save()
            # иначе - создаем новую позицию товара в корзине
            else:
                CartItem.objects.create(cart=self.user_cart, product=product, quantity=self.cart[id]['quantity'])
 
 
    def remove(self, product_id, request):
        product = Products.objects.get(pk=product_id)
        cart_user = CartUser.objects.get(user=request.user)
        cart_item = CartItem.objects.get(cart=cart_user, product=product)
        cart_item.delete()
 
 
    # метод подсчета товаров в корзине
    def _len_(self):
        return sum(int(item['quantity']) for item in self.cart.values())
 
 
     # создание итератора для элементов корзины (чтобы можно было проходиться по элементам в цикле)
    def _iter_(self):
        product_ids = self.cart.keys()
        products = Products.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        # добавление в словарь корзины объекта товара с ключом "product"
        for product in products:
            cart[str(product.id)]['product'] = product
        # добавление в словарь корзины стоимости позиции товара с учетом количества
        for item in cart.values():
            item['total_price'] = item['product'].price * int(item['quantity'])
            yield item
 
 
    # метод подсчета общей стоимости товаров в корзине
    def get_total_price(self):
        return sum(Decimal(item['price']) * int(item['quantity']) for item in self.cart.values())
 
 
# добавление товара в корзину методом POST
@require_POST
def add_cart_db(request, product_id):
    # получаем объект корзины
    cart = ProductCartUser(request)
    # получаем продукт из запроса по его ИД 
    product = get_object_or_404(Products, id=product_id)
    # получаем объект заполненной формы со странички
    form = CartAddProductForm(request.POST)
 
    # если форма заполнена правильно        
    if form.is_valid():
        cd = form.cleaned_data
        # вызываем метод добавления товара в корзину с введенным в поле количеством
        cart.add(product=product, 
                 quantity=cd['quantity'],
                 override_quantity=cd['override'])
    # если форма не заполнена
    else:
        # добавляем  1 единицу товара
        cart.add(product=product, 
                 quantity=1,
                 override_quantity=False)
    # переходим на страницу корзины
    return redirect('cart:cart-detail')
 
 
# удаление товара из корзины
@require_POST
def remove_from_db(request, product_id):
    cart = ProductCartUser(request)
    del cart.cart[str(product_id)]
 
    cart.remove(product_id, request)    
 
    return redirect('cart:cart-detail')