from django import forms
from .models import Order

# способ оплаты
PAYMENT_CHOICES = (
    ("cash", "Наличными"),
    ("card_online", "Картой онлайн"),
    ("card_courier", "Картой курьеру"),
)
# выбор доставки 
DELIVERY_CHOICES = (
    ("pick_up_point", "Пункт выдачи"),
    ("delivery", "Курьерская доставка"),
    ("mail", "Почта России"),
    ("cdek", "СДЭК"),
)

class OrderForm(forms.ModelForm):
    payment  = forms.ChoiceField(choices=PAYMENT_CHOICES, label='Способ оплаты')
    deliviry = forms.ChoiceField(choices=DELIVERY_CHOICES, label='Способ Доставки')
    
    class Meta:
        model = Order
        exclude = ['number', 'status', 'total_price']
        # выбранные поля не включаем в модель заказа 
        # если  fields = то указываем выводимые поля 