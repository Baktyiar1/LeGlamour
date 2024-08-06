from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_views, name='index'),
    path('detail/<int:pk>/', views.detail_views, name='detail'),
    path('shop/', views.shop_view, name='shop'),

    path('about/',views.about_views,name='about'),


]
