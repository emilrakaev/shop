from django import forms
from .models import Product, Basket, Order


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'amount', 'price']


class BasketForm(forms.Form):
    quantity = forms.IntegerField(min_value=0, required=True, label='')


class SimpleSearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label='Поиск')


class OrderForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, label='Имя')
    phone = forms.CharField(max_length=100, required=True, label='Телефон')
    adress = forms.CharField(max_length=100, required=True, label='Адресс')


