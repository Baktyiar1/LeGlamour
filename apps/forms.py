from django import forms
from .models import Cosmetic

class MyUpdateForm(forms.ModelForm):

    class Meta:
        model = Cosmetic
        fields = (
            'title',
            'description',
            'price',
            'brand',
            'image',
            'category',
            'quantity'
        )


class CosmeticAddForm(forms.ModelForm):

    class Meta:
        model = Cosmetic
        fields = (
            'title',
            'description',
            'price',
            'brand',
            'image',
            'category',
            'quantity'
        )
