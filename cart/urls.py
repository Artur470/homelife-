from django.urls import path
from cart.views import *
from django.views.decorators.cache import cache_page


urlpatterns = [

    path('carts/', CartView.as_view(), name='cart'),
    path('order/', CreateOrderView.as_view(), name='cart'),


]