from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotAllowed
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView

from webapp.base_views import SearchView
from webapp.models import Product
from webapp.forms import ProductForm, SimpleSearchForm, BasketForm

from django.contrib import messages


class IndexView(SearchView):
    template_name = 'index.html'
    context_object_name = 'products'
    model = Product
    paginate_by = 3
    paginate_orphans = 0
    search_fields = ['name__icontains']
    ordering = ['category', 'name']

    # def get_query(self, search):
    #     query = Q(name__icontains=search)
    #     return query

    def dispatch(self, request, *args, **kwargs):
        self.test_session_key()
        self.test_session_data()
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().filter(amount__gt=0)

    def test_session_key(self):
        print(self.request.session.session_key)
        if not self.request.session.session_key:
            self.request.session.save()

    def test_session_data(self):
        if 'check' not in self.request.session:
            self.request.session['check'] = 0
        self.request.session['check'] += 1
        print(self.request.session['check'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = BasketForm
        return context


class ProductView(DetailView):
    template_name = 'product/product_view.html'
    model = Product

    # def get_queryset(self):
    #     return super().get_queryset().filter(amount__gt=0)


class ProductCreateView(CreateView):
    template_name = 'product/product_create.html'
    form_class = ProductForm
    model = Product
    permission_required = 'webapp.add_product'

    def get_success_url(self):
        return reverse('webapp:product_view', kwargs={'pk': self.object.pk})


class ProductUpdateVIew(UpdateView):
    template_name = 'product/product_update.html'
    model = Product
    form_class = ProductForm
    permission_required = 'webapp.change_product'

    def get_success_url(self):
        return reverse('webapp:product_view', kwargs={'pk': self.object.pk})


class ProductDeleteView(DeleteView):
    template_name = 'product/product_delete.html'
    model = Product
    success_url = reverse_lazy('webapp:index')
    permission_required = 'webapp.delete_product'


def product_search_view(request):
    query = request.GET.get("searching")
    data = Product.objects.filter(name__icontains=query)
    return render(request, 'product/product_search.html', context={
        'products': data
    })
