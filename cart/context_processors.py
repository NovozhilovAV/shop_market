from .views import Cart
# импортируем класс из views

def cart(request):
    return {'cart': Cart(request)}
# вернули словарь - объект корзины