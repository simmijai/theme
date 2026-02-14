from django.urls import path
from apps.core import page_views

urlpatterns = [
    # path('', page_views.HomeView.as_view(), name='home'),
    path('category/', page_views.CategoryView.as_view(), name='category_all'),
    path('category/<slug:slug>/', page_views.CategoryView.as_view(), name='category'),
    path('product/<slug:slug>/', page_views.ProductDetailView.as_view(), name='product_detail'),
    path('about-us/', page_views.about_us, name='about_us'),
    path('payment-policy/', page_views.payment_policy, name='payment_policy'),
    path('terms-conditions/', page_views.terms_conditions, name='terms_conditions'),
    path('return-refund/', page_views.return_refund, name='return_refund'),
    path('shipping-policy/', page_views.shipping_policy, name='shipping_policy'),
    path('warranty/', page_views.warranty, name='warranty'),
]