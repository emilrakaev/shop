from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import F, Sum, ExpressionWrapper as E

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
    product = models.ForeignKey('webapp.Product', on_delete=models.CASCADE, related_name='buskets')
    quantity = models.IntegerField(verbose_name='Количество')
    session = models.ForeignKey('sessions.Session', on_delete=models.CASCADE, related_name='basket', null=True)

    @classmethod
    def get_with_total(cls):
        # запрос, так быстрее
        total_output_field = models.DecimalField(max_digits=10, decimal_places=2)
        total_expr = E(F('quantity') * F('product__price'), output_field=total_output_field)
        return cls.objects.annotate(total=total_expr)

    @classmethod
    def get_with_product(cls):
        return cls.get_with_total().select_related('product')

    # def total(self):
    #     return self.quantity * self.product.price

    # @classmethod
    # def get_with_total(cls):
    #     total_output_field = models.DecimalField(max_digits=10, decimal_places=2)
    #     total_expr = E(F('qty') * F('product_price'), output_field=total_output_field)
    #     return cls.objects.annotate(total=total_expr)

    # @classmethod
    # def get_with_product(cls):
    #     return cls.get_with_total().select_related('product')

    @classmethod
    def get_cart_total(cls, session_key=None):
        # запрос, так быстрее
        cart_products = cls.get_with_total()
        if session_key:
            cart_products = cart_products.filter(session_id=session_key)
        total = cart_products.aggregate(cart_total=Sum('total'))
        return total['cart_total']

    @classmethod
    def update_session_key(cls, old_id, new_id):
        cls.objects.filter(session_id=old_id).update(session_id=new_id)

    def __str__(self):
        return f'{self.product} - {self.quantity}'

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


class Order(models.Model):
    products = models.ManyToManyField(
        'webapp.Product', related_name='orders', verbose_name='Продукты',
        through='webapp.OrderProduct',
        through_fields=('id_order', 'id_product', 'quantity')
    )
    name = models.CharField(max_length=100, verbose_name='Имя')
    phone = models.CharField(max_length=100, verbose_name='Телефон')
    adress = models.CharField(max_length=100, verbose_name='Адресс')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    user = models.ForeignKey(get_user_model(), null=True, blank=True, on_delete=models.CASCADE, related_name='orders',
                             verbose_name='Пользователь')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def total_order(self):
        total = 0
        for i in self.id_orders.all():
            total += i.total()
        return total


class OrderProduct(models.Model):
    id_order = models.ForeignKey(
        'webapp.Order', related_name='id_orders', on_delete=models.CASCADE,
        verbose_name='Id заказа'
    )
    id_product = models.ForeignKey(
        'webapp.Product', related_name='id_products', on_delete=models.CASCADE,
        verbose_name='Id продукта'
    )
    quantity = models.IntegerField(verbose_name='Количество')

    def __str__(self):
        return f"{self.id_order.name}-{self.id_product.name}-{self.quantity}"

    class Meta:
        verbose_name = 'ЗаказПродукт'
        verbose_name_plural = 'ЗаказыПродукты'

    def total(self):
        return self.id_product.price * self.quantity
