from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_views, name='index'),
    path('detail/<int:pk>/', views.detail_views, name='detail'),
    path('shop/', views.shop_view, name='shop'),
    path('cart/data/', views.get_cart_data, name='get_cart_data'),
    path('add-to-cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('create_order/', views.create_order, name='create_order')
]
