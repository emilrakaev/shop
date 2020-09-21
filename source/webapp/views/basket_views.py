from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, ListView, DeleteView
from django.views.generic.base import View
from django.core.exceptions import ObjectDoesNotExist
from webapp.forms import BasketForm, OrderForm, BasketAddForm
from webapp.models import Basket, Product


class BasketAddView(CreateView):
    model = Basket
    form_class = BasketAddForm

    def post(self, request, *args, **kwargs):
        self.product = get_object_or_404(Product, pk=self.kwargs.get('pk'))
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        quantity = form.cleaned_data.get('quantity', 1)

        try:
            cart_product = Basket.objects.get(product=self.product, session_id=self.get_session_key())
            cart_product.quantity += quantity
            if cart_product.quantity <= self.product.amount:
                cart_product.save()
                messages.add_message(self.request, messages.SUCCESS,
                                     f'Добавлено {self.product.name} - {cart_product.quantity} штук')
            else:
                messages.add_message(self.request, messages.ERROR, 'Фиаско!!!')
        except Basket.DoesNotExist:
            if quantity <= self.product.amount:
                Basket.objects.create(product=self.product, quantity=quantity, session_id=self.get_session_key())
                messages.add_message(self.request, messages.SUCCESS,
                                     f'Добавлено {self.product.name} - {quantity} штук')
            else:
                messages.add_message(self.request, messages.ERROR, 'Фиаско!!!')
        return redirect(self.get_success_url())

    def get_session_key(self):
        session = self.request.session
        if not session.session_key:
            session.save()
        return session.session_key

    def form_invalid(self, form):
        return redirect(self.get_success_url())

    def get_success_url(self):
        # бонус
        next = self.request.GET.get('next')
        if next:
            return next
        return reverse('webapp:index')


class BasketView(ListView):
    template_name = 'basket/basket_view.html'
    # model = Basket
    context_object_name = 'baskets'

    def get_queryset(self):
        return Basket.get_with_product().filter(session_id=self.get_session_key())

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['all'] = Basket.get_cart_total(session_key=self.get_session_key())
        context['form'] = OrderForm()
        return context

    def get_session_key(self):
        session = self.request.session
        if not session.session_key:
            session.save()
        return session.session_key


class BasketDeleteView(DeleteView):
    model = Basket
    success_url = reverse_lazy('webapp:basket_view')

    def get(self, request, *args, **kwargs):
        basket = self.get_object()
        qty = basket.quantity
        product_name = basket.product.name
        messages.add_message(self.request, messages.WARNING,
                             f'{product_name} {qty} штук')
        return self.delete(request, *args, **kwargs)
