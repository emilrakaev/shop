from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import ListView
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
        if self.request.user.is_authenticated:
            order.user = self.request.user
            order.save()
        Basket.objects.all().delete()
        return redirect('webapp:index')

    def form_invalid(self, form):
        basket = Basket.objects.all()
        context = {
            'baskets': basket,
            'form': form
        }
        return render(self.request, 'basket/basket_view.html', context)


class OrderList(LoginRequiredMixin, ListView):
    template_name = 'order_list.html'
    context_object_name = 'orders'
    model = Order

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        orders = Order.objects.filter(user=self.request.user)
        context['orders'] = orders
        return context
