"""
URL configuration for Ecommerce_website project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from apps.store.views import HomeView
from django.conf import settings
from django.conf.urls.static import static
from apps.admin_panel.views import admin_views
from apps.core import page_views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('accounts/', include('apps.accounts.urls')),
    path('admin_panel/', include('apps.admin_panel.urls')),
    path('cart/', include('apps.cart.urls')),
    path('wishlist/', include('apps.wishlist.urls')),
    path('orders/', include('apps.orders.urls')),
    path('admin-login/', admin_views.admin_login, name='admin_login'),
    path('about-us/', page_views.about_us, name='about_us'),
    path('contact-us/', page_views.contact_us, name='contact'),
    path('payment-policy/', page_views.payment_policy, name='payment_policy'),
    path('terms-conditions/', page_views.terms_conditions, name='terms_conditions'),
    path('return-refund/', page_views.return_refund, name='return_refund'),
    path('shipping-policy/', page_views.shipping_policy, name='shipping_policy'),
    path('warranty/', page_views.warranty, name='warranty'),
    path('', include('apps.products.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
