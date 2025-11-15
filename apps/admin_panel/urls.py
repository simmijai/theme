# admin_panel/urls.py
from django.urls import path
from apps.admin_panel.views import (
    admin_views, category_views, product_views,
    customer_views, order_views, views_slider, admin_reviews
)


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
    
    path('order/<int:order_id>/', customer_views.order_detail, name='order-detail'),
    
    path('admin/orders/', order_views.admin_order_list, name='admin_order_list'),
path('admin/orders/<int:order_id>/update-status/', order_views.update_order_status, name='update_order_status'),



path('sliders/', views_slider.slider_list, name='admin_slider_list'),
    path('sliders/create/', views_slider.slider_create, name='admin_slider_create'),
    path('sliders/edit/<int:slider_id>/', views_slider.slider_edit, name='admin_slider_edit'),
    path('sliders/delete/<int:slider_id>/', views_slider.slider_delete, name='admin_slider_delete'),
    
    path('reviews/', admin_reviews.admin_review_list, name='admin_review_list'),
    path('reviews/edit/<int:review_id>/', admin_reviews.admin_review_edit, name='admin_review_edit'),
    path('reviews/delete/<int:review_id>/', admin_reviews.admin_review_delete, name='admin_review_delete'),
    path('reviews/toggle/<int:review_id>/', admin_reviews.admin_review_toggle, name='admin_review_toggle'),



]


