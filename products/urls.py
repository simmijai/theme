from django.urls import path
from . import views

urlpatterns = [
    path('category/<slug:slug>/', views.category_products, name='category_products'),
]
