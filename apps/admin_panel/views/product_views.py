from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView
from django.db.models import Q
from apps.products.models import Product, ProductImage, Category
from apps.admin_panel.forms import ProductForm, ProductImageForm
from django.contrib import messages

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

class AdminProductListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Product
    template_name = 'admin_theme/products/product.html'
    context_object_name = 'products'
    paginate_by = 5
    
    def get_queryset(self):
        queryset = Product.objects.prefetch_related('images', 'category').all()
        
        # Search by name or SKU
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(sku__icontains=search)
            )
        
        # Filter by category
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category_id=category)
        
        # Filter by availability
        availability = self.request.GET.get('availability')
        if availability == 'available':
            queryset = queryset.filter(is_available=True, stock__gt=0)
        elif availability == 'out_of_stock':
            queryset = queryset.filter(stock=0)
        elif availability == 'unavailable':
            queryset = queryset.filter(is_available=False)
        
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['search'] = self.request.GET.get('search', '')
        context['category'] = self.request.GET.get('category', '')
        context['availability'] = self.request.GET.get('availability', '')
        return context

# Keep FBV for backward compatibility (can be removed later)
# def product_list(request):
#     products = Product.objects.prefetch_related('images', 'category').all()
#     return render(request, 'admin_theme/products/product.html', {'products': products})


def product_create(request):
    try:
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES)
            image_form = ProductImageForm(request.POST, request.FILES)

            if form.is_valid():
                try:
                    product = form.save()
                    
                    # Handle multiple extra images with error handling
                    if 'images' in request.FILES:
                        images = request.FILES.getlist('images')
                        for img in images:
                            try:
                                ProductImage.objects.create(product=product, image=img)
                            except Exception as e:
                                messages.warning(request, f'Error uploading image: {img.name}')
                    
                    messages.success(request, f'Product "{product.name}" created successfully!')
                    return redirect('admin_product_list')
                except Exception as e:
                    messages.error(request, 'Error saving product. Please try again.')
            else:
                # Form has validation errors
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f'{field.replace("_", " ").title()}: {error}')
        else:
            form = ProductForm()
            image_form = ProductImageForm()

        return render(request, 'admin_theme/products/product_create.html', {'form': form, 'image_form': image_form})
    except Exception as e:
        messages.error(request, 'Error loading product form. Please try again.')
        return redirect('admin_product_list')

def product_delete(request, pk):
    try:
        product = get_object_or_404(Product, pk=pk)
        product_name = product.name
        product.delete()
        messages.success(request, f'Product "{product_name}" deleted successfully!')
    except Exception as e:
        messages.error(request, 'Error deleting product. Please try again.')
    return redirect('admin_product_list')

def product_edit(request, pk):
    try:
        product = get_object_or_404(Product, pk=pk)
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES, instance=product)
            image_form = ProductImageForm(request.POST, request.FILES)

            if form.is_valid():
                try:
                    product = form.save()
                    
                    # Handle additional images with error handling
                    if 'images' in request.FILES:
                        for img in request.FILES.getlist('images'):
                            try:
                                ProductImage.objects.create(product=product, image=img)
                            except Exception as e:
                                messages.warning(request, f'Error uploading image: {img.name}')

                    messages.success(request, f'Product "{product.name}" updated successfully!')
                    return redirect('admin_product_list')
                except Exception as e:
                    messages.error(request, 'Error updating product. Please try again.')
            else:
                # Form has validation errors
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f'{field.replace("_", " ").title()}: {error}')
        else:
            form = ProductForm(instance=product)
            image_form = ProductImageForm()

        return render(request, 'admin_theme/products/product_create.html', {
            'form': form,
            'image_form': image_form,
            'action': 'Edit',
        })
    except Exception as e:
        messages.error(request, 'Error loading product. Please try again.')
        return redirect('admin_product_list')


def product_image_delete(request, pk):
    try:
        img = get_object_or_404(ProductImage, pk=pk)
        product_id = img.product.id
        img.delete()
        messages.success(request, "Image deleted successfully!")
    except Exception as e:
        messages.error(request, 'Error deleting image. Please try again.')
        product_id = pk  # fallback
    return redirect('admin_product_edit', pk=product_id)
