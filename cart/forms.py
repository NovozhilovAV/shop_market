from django import forms

# QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 10)]

# class CartAddProductForm(forms.Form):
#     quantity = forms.TypedChoiceField(choices=QUANTITY_CHOICES, coerce=int, label='Количество')
#     override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)


class CartAddProductForm(forms.Form):
    
    quantity = forms.IntegerField(
        max_value=1000, 
        min_value=1,
        label='Количество',
        widget=forms.NumberInput(attrs={'style':'width:80px', 'id':'quantity', 'onchange':"sendCount(this)"}),
        initial=1
        )
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)