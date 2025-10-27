from django.urls import path
from . import views

urlpatterns = [
    path('category/<slug:slug>/', views.category_products, name='category_products'),
    path('filter/<slug:slug>/', views.filter_products_ajax, name='filter_products_ajax'),
    path('<slug:category_slug>/<slug:product_slug>/',views.product_detail',name="product_detail"),
]
