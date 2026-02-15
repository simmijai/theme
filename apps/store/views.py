from .models import HomeSlider
from apps.products.models import Product,Category
from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = 'user_theme/store/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sliders'] = HomeSlider.objects.filter(is_active=True)
        context['categories'] = Category.objects.filter(is_active=True)[:6]
        context['featured_products'] = Product.objects.filter(is_available=True)[:8]
        context['best_selling_products'] = Product.objects.filter(is_available=True)[:8]
        return context