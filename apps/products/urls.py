from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search_products_view, name='search_products'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('product/<int:product_id>/review/', views.add_or_edit_review, name='add_or_edit_review'),
    path('review/<int:review_id>/delete/', views.delete_review, name='delete_review'),
    path('<slug:slug>/', views.category_products, name='category_products'),
]
