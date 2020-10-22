# from django.contrib.auth import get_user_model
# from rest_framework import serializers
#
# from webapp.models import Product, Order, OrderProduct, Basket
#
#
# class ProductSerializer(serializers.ModelSerializer):
#     url = serializers.HyperlinkedIdentityField(read_only=True,
#                                                view_name='api_v1:product-detail')
#
#     class Meta:
#         model = Product
#         fields = ['id', 'url', 'name', 'description', 'category', 'amount', 'price']
#
#
# class OrderProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OrderProduct
#         fields = ['id_order','id_product', 'quantity']
#
# class ProductQtySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OrderProduct
#         fields = ['id_product', 'quantity']
#
# class OrderSerializer(serializers.ModelSerializer):
#     product_display = ProductQtySerializer(many=True,  source='products')
#     class Meta:
#         model = Order
#         fields = ['product_display', 'name', 'phone', 'adress']
#     def create_orders(self):
#         print(self.data)
#         order = Order.objects.create(name=self.data['name'],phone=self.data['phone'],adress=self.data['adress'])
#         for product in self.data['id_orders']:
#             product_order = OrderProductSerializer(data={
#                 'id_order': order['pk'],
#                 'id_product': product['product'].pk,
#                 'quantity': product['quantity']
#             })
#             if product_order.is_valid():
#                 print(product_order)
#                 product_order.save()
#
# class UserSerializer(serializers.ModelSerializer):
#     url = serializers.HyperlinkedIdentityField(read_only=True, view_name='api_v1:user-detail')
#
#     class Meta:
#         model = get_user_model()
#         fields = ['id', 'url', 'username', 'first_name', 'last_name', 'email']
#
#
# class BasketSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Basket
#         fields = ['product', 'quantity']


from django.contrib.auth import get_user_model
from rest_framework import serializers

from webapp.models import Product, Order, OrderProduct, Basket


class ProductSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(read_only=True,
                                               view_name='api_v1:product-detail')

    class Meta:
        model = Product
        fields = ['id', 'url', 'name', 'description', 'category', 'amount', 'price']


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ['id_product','id_order', 'quantity']


class UserSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api_v1:user-detail')

    class Meta:
        model = get_user_model()
        fields = ['id', 'url', 'username', 'first_name', 'last_name', 'email']

class OrderSerializer(serializers.ModelSerializer):
    id_orders = OrderProductSerializer(many=True, required=False)

    class Meta:
        model = Order
        fields = ['id_orders', 'name', 'phone', 'adress', 'created_at', 'user']





# class BasketSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Basket
#         fields = ['product', 'quantity']
