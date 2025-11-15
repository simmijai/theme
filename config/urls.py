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
from apps.store.views import index
from django.conf import settings
from django.conf.urls.static import static
from apps.admin_panel.views.category_views import admin_dashboard



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='home'),  # homepage
    # path('', include('store.urls')),

    path('products/', include('apps.products.urls')),
    path('accounts/', include('apps.accounts.urls')),  # ❌ No namespace

    path('dashboard/', admin_dashboard, name='dashboard'),  # new dashboard
    path('admin_panel/', include('apps.admin_panel.urls')),  # include your admin_panel URLs
    
    path('cart/', include('apps.cart.urls')),
    path('wishlist/', include('apps.wishlist.urls')),
    path('orders/', include('apps.orders.urls')),



    



]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
