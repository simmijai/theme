from django.shortcuts import render, redirect
from products.models import Product, ProductImage
from admin_panel.forms import ProductForm, ProductImageForm
from django.contrib import messages


def product_list(request):
    products = Product.objects.prefetch_related('images', 'category').all()
    return render(request, 'admin/product.html', {'products': products})




# def product_create(request):
#     if request.method == 'POST':
#         print("📩 POST request received")
#         print("🧾 POST keys:", request.POST.keys())
#         print("📂 FILES keys:", request.FILES.keys())

#         form = ProductForm(request.POST, request.FILES)
#         img_form = ProductImageForm(request.POST, request.FILES)

#         if form.is_valid():
#             product = form.save()
#             print("✅ Product form valid")

#             if img_form.is_valid():
#                 print("✅ Image form valid")
#                 images = request.FILES.getlist('images')
#                 for image in images:
#                     ProductImage.objects.create(product=product, image=image)
#             else:
#                 print("⚠️ Image form invalid:", img_form.errors)

#             messages.success(request, f'✅ Product "{product.name}" created successfully!')
#             return redirect('admin_product_list')

#         else:
#             print("❌ Form invalid")
#             print("ProductForm errors:", form.errors)
#             print("ImageForm errors:", img_form.errors)

#     else:
#         form = ProductForm()
#         img_form = ProductImageForm()

#     return render(request, 'admin/product_create.html', {
#         'form': form,
#         'img_form': img_form,
#         'action': 'Add',
#     })

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

    return render(request, 'admin/product_create.html', {'form': form, 'image_form': image_form})