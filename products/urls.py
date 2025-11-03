from django.urls import path
from . import views

urlpatterns = [
    path('category/<slug:slug>/', views.category_products, name='category_products'),
    
    
    path('products/subcategory/<slug:slug>/', views.subcategory_products, name='subcategory_products'),
    
    path('product/<slug:slug>/', views.product_detail, name='product_detail')





    
]
