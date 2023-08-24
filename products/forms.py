from django import forms


class CategoriForm(forms.ModelForm):
    class Meta:
        model = Categori
        fields = '__all__'
        labels = {
            'name' = "Имя",
            'deskription' = 'Описание',
            'slug' = 'URL - адрес',
        }

class SubcategoriForm(forms.ModelForm):
    class Meta:
        