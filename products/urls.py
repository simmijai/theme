from django.urls import path
from . import views

urlpatterns = [
    path('category/<slug:slug>/', views.category_products, name='category_products'),
    
    # path('cart/',views.cart_page,name="cart_page"),
    path('cart1/',views.cart_page1,name="cart_page1"),
    path('checkout/',views.checkout,name="checkout"),
    path('wishlist/',views.wishlist,name="wishlist"),
    
    path('products/subcategory/<slug:slug>/', views.subcategory_products, name='subcategory_products'),
    
    path('product/<slug:slug>/', views.product_detail, name='product_detail')





    
]
