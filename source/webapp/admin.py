from django.contrib import admin
from .models import Product, Order, OrderProduct


class ProductAdmin(admin.ModelAdmin):
    list_filter = ('category',)
    list_display = ('pk', 'name', 'amount', 'price')
    list_display_links = ('pk', 'name')
    search_fields = ('name',)


class OrderProductAdmin(admin.TabularInline):
    model = OrderProduct
    fields = ['id_product', 'quantity']
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display_links = ['pk', 'name']
    list_display = ('pk', 'name', 'phone', 'created_at')
    ordering = ['-created_at']
    inlines = (OrderProductAdmin,)


admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct)
