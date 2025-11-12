# admin_panel/urls.py
from django.urls import path
from admin_panel.views import admin_views, category_views,product_views,customer_views
# from . import views

urlpatterns = [
    # Dashboard & Others
    path('dashboard/', admin_views.admin_dashboard, name='admin_dashboard'),
    path('subcategory/list/', admin_views.admin_subcategory_list, name='admin_subcategory_list'),
    path('customer/<int:customer_id>/', customer_views.customer_details, name='customer_details'),

    # Category CRUD (Class-based)
    path('category/list/', category_views.CategoryListView.as_view(), name='admin_category_list'),
    path('category/add/', category_views.CategoryCreateView.as_view(), name='admin_category_create'),
    path('category/update/<int:pk>/', category_views.CategoryUpdateView.as_view(), name='admin_category_update'),
    path('category/delete/<int:pk>/', category_views.CategoryDeleteView.as_view(), name='admin_category_delete'),
    
    
    path('products/', product_views.product_list, name='admin_product_list'),
    path('products/add/', product_views.product_create, name='admin_product_create'),
    path('products/edit/<int:pk>/', product_views.product_edit, name='admin_product_edit'),


    path('products/delete/<int:pk>/', product_views.product_delete, name='admin_product_delete'),

    path('products/image/delete/<int:pk>/', product_views.product_image_delete, name='admin_product_image_delete'),

    path('customer/list/', customer_views.customer_list, name='customer_list'),
]
