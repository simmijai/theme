from django.shortcuts import render, redirect
from apps.products.models import Product, ProductImage
from apps.admin_panel.forms import ProductForm, ProductImageForm
from django.contrib import messages


def product_list(request):
    products = Product.objects.prefetch_related('images', 'category').all()
    return render(request, 'admin_theme/products/product.html', {'products': products})


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
    product = Product.objects.get(pk=pk)
    product.delete()
    messages.success(request, f'Product "{product.name}" deleted successfully!')
    return redirect('admin_product_list')

def product_edit(request, pk):
    product = Product.objects.get(pk=pk)
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
    img = ProductImage.objects.get(pk=pk)
    product_id = img.product.id
    img.delete()
    messages.success(request, "Image deleted successfully!")
    return redirect('admin_product_edit', pk=product_id)
