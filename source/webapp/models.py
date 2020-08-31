from django.core.validators import MinValueValidator
from django.db import models

DEFAULT_CATEGORY = 'other'
CATEGORY_CHOICES = [
    (DEFAULT_CATEGORY, 'Разное'),
    ('food', 'Продукты питания'),
    ('household', 'Хоз. товары'),
    ('toys', 'Детские игрушки'),
    ('appliances', 'Бытовая Техника')
]


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(max_length=2000, null=True, blank=True, verbose_name='Описание')
    category = models.TextField(max_length=20, choices=CATEGORY_CHOICES,
                                default=DEFAULT_CATEGORY, verbose_name='Категория')
    amount = models.IntegerField(verbose_name='Остаток', validators=[MinValueValidator(0)])
    price = models.DecimalField(verbose_name='Цена', max_digits=7, decimal_places=2)

    def __str__(self):
        return f'{self.name} - {self.amount}'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['name', 'category']


class Basket(models.Model):
    product = models.ForeignKey('webapp.Product', on_delete=models.CASCADE, related_name='Продукт')
    quantity = models.IntegerField(verbose_name='Количество')

    def total(self):
        return self.quantity * self.product.price



