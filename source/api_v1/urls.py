from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api_v1.views import ProductViewSet, OrderList, OrderView

app_name = 'api_v1'

router = DefaultRouter()
router.register(r'product', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('orders/', OrderList.as_view(), name='order_list'),
    path('order/', OrderView.as_view(), name='order'),
]