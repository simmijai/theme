from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from apps.products.models import Product, Category
from apps.store.models import HomeSlider


class HomeView(TemplateView):
    template_name = 'user_theme/pages/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sliders'] = HomeSlider.objects.filter(is_active=True)
        context['categories'] = Category.objects.filter(is_active=True)[:6]
        context['featured_products'] = Product.objects.filter(is_available=True)[:8]
        context['best_selling_products'] = Product.objects.filter(is_available=True)[:8]
        return context


class CategoryView(TemplateView):
    template_name = 'user_theme/pages/category.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')
        
        if slug:
            category = get_object_or_404(Category, slug=slug, is_active=True)
            products = Product.objects.filter(category=category, is_available=True)
        else:
            category = None
            products = Product.objects.filter(is_available=True)
            
        context['category'] = category
        context['products'] = products
        context['categories'] = Category.objects.filter(is_active=True)
        return context


class ProductDetailView(TemplateView):
    template_name = 'user_theme/pages/product_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')
        product = get_object_or_404(Product, slug=slug, is_available=True)
        
        context['product'] = product
        context['related_products'] = Product.objects.filter(
            category=product.category, 
            is_available=True
        ).exclude(id=product.id)[:6]
        return context
