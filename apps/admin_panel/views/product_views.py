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
    if request.method == 'POST':
        print("POST request received")
        print("🧾 POST keys:", request.POST.keys())
        print("📂 FILES keys:", request.FILES.keys())

        form = ProductForm(request.POST, request.FILES)
        image_form = ProductImageForm(request.POST, request.FILES)

        if form.is_valid():
            product = form.save()  # save main product
            print("✅ Product saved:", product.name)

            # ✅ Handle multiple extra images
            if 'images' in request.FILES:
                images = request.FILES.getlist('images')
                print(request.FILES)
                print(request.FILES.getlist('images'))

                
                for img in images:
                    ProductImage.objects.create(product=product, image=img)
                print(f"✅ {len(images)} extra images saved.")
            else:
                print("⚠️ No extra images found in FILES")

            return redirect('admin_product_list')
        else:
            print("❌ Form invalid")
            print(form.errors)
    else:
        form = ProductForm()
        image_form = ProductImageForm()

    return render(request, 'admin_theme/products/product_create.html', {'form': form, 'image_form': image_form})

def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    messages.success(request, f'Product "{product.name}" deleted successfully!')
    return redirect('admin_product_list')

def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        image_form = ProductImageForm(request.POST, request.FILES)

        if form.is_valid():
            product = form.save()
            
            # Handle additional images
            if 'images' in request.FILES:
                for img in request.FILES.getlist('images'):
                    ProductImage.objects.create(product=product, image=img)

            messages.success(request, f'Product "{product.name}" updated successfully!')
            return redirect('admin_product_list')
    else:
        form = ProductForm(instance=product)
        image_form = ProductImageForm()

    return render(request, 'admin_theme/products/product_create.html', {
        'form': form,
        'image_form': image_form,
        'action': 'Edit',
    })


def product_image_delete(request, pk):
    img = get_object_or_404(ProductImage, pk=pk)
    product_id = img.product.id
    img.delete()
    messages.success(request, "Image deleted successfully!")
    return redirect('admin_product_edit', pk=product_id)
