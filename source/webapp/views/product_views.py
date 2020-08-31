from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotAllowed
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView

from webapp.base_views import SearchView
from webapp.models import Product
from webapp.forms import ProductForm, SimpleSearchForm, BasketForm


class IndexView(SearchView):
    template_name = 'index.html'
    context_object_name = 'products'
    model = Product
    paginate_by = 3
    paginate_orphans = 0
    search_form = SimpleSearchForm
    ordering = ['category', 'name']

    def get_query(self, search):
        query = Q(name__icontains=search)
        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = BasketForm
        return context


class ProductView(DetailView):
    template_name = 'product/product_view.html'
    model = Product


class ProductCreateView(CreateView):
    template_name = 'product/product_create.html'
    form_class = ProductForm
    model = Product

    def get_success_url(self):
        return reverse('product_view', kwargs={'pk': self.object.pk})


class ProductUpdateVIew(UpdateView):
    template_name = 'product/product_update.html'
    model = Product
    form_class = ProductForm

    def get_success_url(self):
        return reverse('product_view', kwargs={'pk': self.object.pk})


class ProductDeleteView(DeleteView):
    template_name = 'product/product_delete.html'
    model = Product
    success_url = reverse_lazy('index')


def product_search_view(request):
    query = request.GET.get("searching")
    data = Product.objects.filter(name__icontains=query)
    return render(request, 'product/product_search.html', context={
        'products': data
    })
