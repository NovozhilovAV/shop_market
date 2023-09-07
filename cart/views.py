from market import settings
from products.models import Products
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from products.models import Products
from .forms import CartAddProductForm

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

        # корзина, продукты, количество...
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
# @require_POST
# def cart_add(request, product_id):
#     cart = Cart(request)
#     product = get_object_or_404(Products, id=product_id)
#     form = CartAddProductForm(request.POST)
    
#     if form.is_valid():
#         cd = form.cleaned_data
#         cart.add(product=product, 
#                  quantity=cd['quantity'],
#                  override_quantity=cd['override'])
    
#     return redirect('cart:cart-detail')



# @require_POST
# def cart_remove(request, product_id):
#     cart = Cart(request)
#     product = get_object_or_404(Products, id=product_id)
#     cart.remove(product)
    
#     return redirect('cart:cart-detail')


# def cart_detail(request):
#     cart = Cart(request)
#     for item in cart:
#         item['update_quantity_form'] = CartAddProductForm(initial={
#             'quantity': item['quantity'],
#             'override': True})
#     return render(request, 'cart/cart-detail.html', {'cart': cart})