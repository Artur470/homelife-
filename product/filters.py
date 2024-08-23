import django_filters
from .models import Product


class ProductFilter(django_filters.FilterSet):
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte', label='Цена от')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte', label='Цена до')

    class Meta:
        model = Product
        fields = {
            'title': ['icontains'],
            'category': ['exact'],
            'brand': ['exact'],
            'color': ['exact'],
        }
