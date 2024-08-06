from django import forms
from .models import Cosmetic


class CosmeticsUpdateform(forms.ModelForm):

    class Meta:
        model = Cosmetic
        fields = (
            'title',
            'description',
            'price',
            'brand',
            'image',
            'quantity',
            'is_active',
            'create_date',
            'update_date',
        )