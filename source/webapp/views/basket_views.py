from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, DeleteView
from django.views.generic.base import View
from django.core.exceptions import ObjectDoesNotExist
from webapp.forms import BasketForm, OrderForm
from webapp.models import Basket, Product


class BasketAddView(View):
    redirect_url = ''

    def post(self, request, *args, **kwargs):
        form = BasketForm(data=request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        product = get_object_or_404(Product, pk=self.kwargs.get('pk'))
        qty = form.cleaned_data['quantity']

        if qty > product.amount:
            return redirect('index')
        elif product.amount == 0:
            return redirect('index')
        else:
            try:
                basket = Basket.objects.get(product=product.pk)
                basket.quantity += qty
                basket.save()
                return redirect('index')
            except ObjectDoesNotExist:
                Basket.objects.create(product=product, quantity=qty)
                return redirect('index')

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        return redirect('index')

    def get_context_data(self, **kwargs):
        return kwargs

    def get_redirect_url(self):
        return self.redirect_url


class BasketView(ListView):
    template_name = 'basket/basket_view.html'
    model = Basket
    context_object_name = 'baskets'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['all'] = 0
        context['form'] = OrderForm()
        for i in Basket.objects.all():
            context['all'] += i.total()
        return context


class BasketDeleteView(DeleteView):
    model = Basket
    success_url = reverse_lazy('basket_view')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
