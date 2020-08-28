from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'amount', 'price']


class SimpleSearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label='Поиск')
