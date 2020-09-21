"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from webapp.views.basket_views import BasketAddView, BasketView, BasketDeleteView
from webapp.views.order_views import OrderView, OrderList
from webapp.views.product_views import IndexView, ProductView, \
    ProductCreateView, ProductUpdateVIew, ProductDeleteView
from django.conf.urls.static import static

app_name = 'webapp'
urlpatterns = [

    path('', IndexView.as_view(), name='index'),
    path('product/add/', ProductCreateView.as_view(), name='product_create'),
    path('product/<int:pk>/', ProductView.as_view(), name='product_view'),
    path('product/<int:pk>/update/', ProductUpdateVIew.as_view(), name='product_update'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),

    path('product/basket/<int:pk>/add', BasketAddView.as_view(), name='add_basket'),
    path('basket/', BasketView.as_view(), name='basket_view'),
    path('basket/<int:pk>/delete/', BasketDeleteView.as_view(), name='delete_view'),

    path('order/', OrderView.as_view(), name='order_view'),
    path('orders/', OrderList.as_view(), name='order_list'),

]
