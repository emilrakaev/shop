from django.shortcuts import redirect, render
from django.views.generic import CreateView
from django.views.generic import View
from webapp.forms import OrderForm
from webapp.models import Order, Basket, OrderProduct, Product


class OrderView(View):

    def post(self, request, *args, **kwargs):
        form = OrderForm(data=request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        order = Order.objects.create(**form.cleaned_data)
        for i in Basket.objects.all():
            OrderProduct.objects.create(id_order=order, id_product=i.product, quantity=i.quantity)
            product = Product.objects.get(pk=i.product.pk)
            product.amount -= i.quantity
            product.save()
        Basket.objects.all().delete()
        return redirect('index')

    def form_invalid(self, form):
        basket = Basket.objects.all()
        context = {
            'baskets': basket,
            'form': form
        }
        return render(self.request, 'basket/basket_view.html', context)
