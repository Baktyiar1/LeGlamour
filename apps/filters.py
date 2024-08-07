import django_filters
from .models import Cosmetic
from django import forms

class CosmeticFilters(django_filters.FilterSet):
    price__gt = django_filters.NumberFilter(field_name='price', lookup_expr='gte', label='Цена от')
    price__lt = django_filters.NumberFilter(field_name='price', lookup_expr='lte', label='Цена до')
    title = django_filters.CharFilter(field_name='title',lookup_expr='icontains', label='Название')
    brand = django_filters.CharFilter(field_name='brand',lookup_expr='icontains',  label='Бренд')

    class Meta:
        model = Cosmetic
        fields = (
            'price__gt',
            'price__lt',
            'title',
            'brand'
        )
