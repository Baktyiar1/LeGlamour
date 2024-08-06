import django_filters
from .models import Cosmetic
from django import forms

class CosmeticFilters(django_filters.FilterSet):
    price__gt = django_filters.NumberFilter(field_name='price', lookup_expr='gte', label='Цена от')
    price__lt = django_filters.NumberFilter(field_name='price', lookup_expr='lte', label='Цена до')

    class Meta:
        model = Cosmetic
        fields = ('price__gt', 'price__lt')
