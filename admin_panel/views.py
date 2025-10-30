from django.shortcuts import render

def admin_dashboard(request):
    return render(request, 'admin/dashboard.html')


# Render form to create a new category
def admin_category_create(request):
    return render(request, 'admin/category_add.html')  # show add form

# Render list of categories
def admin_category_list(request):
    return render(request, 'admin/category.html')  # show category list

def admin_product(request):
    return render(request, 'admin/product.html')

def admin_product_create(request):
    return render(request, 'admin/product_create.html')

def admin_subcategory_list(request):
    return render(request, 'admin/subcategory.html')

def customer_details(request):
    return render(request, 'admin/customer_details.html')