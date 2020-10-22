from django.shortcuts import get_object_or_404
from rest_framework.permissions import SAFE_METHODS, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from api_v1.serializers import ProductSerializer, OrderProductSerializer, OrderSerializer
from webapp.models import Product, Order, Basket


class ProductViewSet(ViewSet):
    queryset = Product.objects.all()
    permission_classes = [IsAdminUser]

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return []
        return super().get_permissions()

    def list(self, request):
        objects = Product.objects.all()
        slr = ProductSerializer(objects, many=True, context={'request': request})
        return Response(slr.data)

    def create(self, request):
        user = request.user
        slr = ProductSerializer(data=request.data)
        if slr.is_valid():
            product = slr.save()
            return Response(slr.data)
        else:
            return Response(slr.errors, status=400)

    def retrieve(self, request, pk=None):
        product = get_object_or_404(Product, pk=pk)
        slr = ProductSerializer(product, context={'request': request})
        return Response(slr.data)

    def update(self, request, pk=None):
        product = get_object_or_404(Product, pk=pk)
        slr = ProductSerializer(data=request.data, instance=product)
        if slr.is_valid():
            product = slr.save()
            return Response(slr.data)
        else:
            return Response(slr.errors, status=400)

    def destroy(self, request, pk=None):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response({'pk': pk})


class OrderList(APIView):
    def get(self, request, *args, **kwargs):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True, context={'request': request})
        return Response(serializer.data)


class OrderView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = OrderSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            order = serializer.save()
            session = self.request.session
            print(session)
            carts = Basket.objects.filter(session=session.session_key)
            print(carts)
            for cart in carts:
                order_product = OrderProductSerializer(
                    data={'id_product': cart.product_id, 'id_order': order.pk, 'quantity': cart.quantity})
                if order_product.is_valid():
                    order_product.save()
                cart.delete()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)

    def get_permissions(self):
        if self.request.method not in SAFE_METHODS:
            return []
        return super().get_permissions()

# class OrderView(APIView):
#     def post(self, request, *args, **kwargs):
#         serializer = OrderSerializer(data=request.data)
#         if serializer.is_valid():
#             print(serializer.is_valid())
#             serializer.create_orders()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=400)


# class BasketAddView(APIView):
#     def post(self, request, *args, **kwargs):
#         product = get_object_or_404(Product, pk=kwargs['pk'])
#         serializer = BasketSerializer(data=request.data, instance=product)
#         qty = serializer['quantity']
#         try:
#             cart_product = Basket.objects.get(product=product)
#             cart_product.quantity += qty
#             if cart_product.quantity <= product.amount:
#                 serializer = BasketSerializer(cart_product)
#                 serializer.save()
#                 return Response(serializer.data)
#         except Basket.DoesNotExist:
#             if qty <= product.amount:
#                 serializer.save()
#             else:
#                 Response({"error": "error amount"})


# def form_valid(self, form):
#     order = Order.objects.create(**form.cleaned_data)
#     for i in Basket.objects.all():
#         OrderProduct.objects.create(id_order=order, id_product=i.product, quantity=i.quantity)
#         product = Product.objects.get(pk=i.product.pk)
#         product.amount -= i.quantity
#         product.save()
#     if self.request.user.is_authenticated:
#         order.user = self.request.user
#         order.save()
#     Basket.objects.all().delete()
#     return redirect('webapp:index')
#
# def form_invalid(self, form):
#     basket = Basket.objects.all()
#     context = {
#         'baskets': basket,
#         'form': form
#     }
#     return render(self.request, 'basket/basket_view.html', context)
