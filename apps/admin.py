from django.contrib import admin

from .models import Cosmetic, Order, Category, Cart, CartItem

admin.site.register(Cosmetic)
admin.site.register(Order)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(CartItem)
