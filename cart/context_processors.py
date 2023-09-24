from .views import Cart, ProductCartUser
# импортируем класс из views

def cart(request):
    if request.user.id:
        return {'cart': ProductCartUser(request)}
# вернули словарь - объект корзины
    return {'cart': Cart(request)}

