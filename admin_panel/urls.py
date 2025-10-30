from django.urls import path
from . import views


urlpatterns = [
    path('category/add/', views.admin_category_create, name='admin_category_create'),
    path('category/list/', views.admin_category_list, name='admin_category_list'),
    path('product/add/', views.admin_product, name='admin_product'),
    path('product/list/', views.admin_product_create, name='admin_product_create'),
    path('subcategory/list/', views.admin_subcategory_list, name='admin_subcategory_list'),
    path('customer_details/', views.customer_details, name='customer_details'),



        
]
