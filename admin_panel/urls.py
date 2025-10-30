# admin_panel/urls.py
from django.urls import path
from admin_panel.views import admin_views, category_views

urlpatterns = [
    # Dashboard & Others
    path('dashboard/', admin_views.admin_dashboard, name='admin_dashboard'),
    path('product/add/', admin_views.admin_product, name='admin_product'),
    path('product/list/', admin_views.admin_product_create, name='admin_product_create'),
    path('subcategory/list/', admin_views.admin_subcategory_list, name='admin_subcategory_list'),
    path('customer_details/', admin_views.customer_details, name='customer_details'),

    # Category CRUD (Class-based)
    path('category/list/', category_views.CategoryListView.as_view(), name='admin_category_list'),
    path('category/add/', category_views.CategoryCreateView.as_view(), name='admin_category_create'),
    path('category/update/<int:pk>/', category_views.CategoryUpdateView.as_view(), name='admin_category_update'),
    path('category/delete/<int:pk>/', category_views.CategoryDeleteView.as_view(), name='admin_category_delete'),
]
