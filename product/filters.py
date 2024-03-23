from django_filters import rest_framework as filters
from .models import Storage


class StorageFilter(filters.FilterSet):
    product__discount = filters.NumberFilter(lookup_expr='gt')
    min_price = filters.NumberFilter(field_name="product__price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="product__price", lookup_expr='lte')

    class Meta:
        model = Storage
        fields = ('status', 'product__price', 'product__discount')


