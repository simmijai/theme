from django.urls import path
from . import views

urlpatterns = [
    path('category/<slug:slug>/', views.category_products, name='category_products'),
    path('filter/<slug:slug>/', views.filter_products_ajax, name='filter_products_ajax'),
    
    path('cart/',views.cart_page,name="cart_page"),
    path('cart1/',views.cart_page1,name="cart_page1"),
    path('checkout/',views.checkout,name="checkout"),


    
]
