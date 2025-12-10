from django.shortcuts import render
from apps.products.models import Category  # make sure Category model exists


# ------------------------
# DASHBOARD
# ------------------------
def admin_dashboard(request):
    return render(request, 'admin_theme/dashboard.html')



# ------------------------
# PRODUCT
# ------------------------
def admin_product(request):
    return render(request, 'admin_theme/products/product.html')


def admin_product_create(request):
    return render(request, 'admin_theme/products/product_create.html')


# ------------------------
# SUBCATEGORY
# ------------------------
def admin_subcategory_list(request, category_id):
    # fetch the parent category
    category = get_object_or_404(Category, id=category_id)
    # fetch subcategories
    subcategories = category.subcategories.all()

    return render(request, 'admin_theme/categories/subcategory.html', {
        'category': category,
        'subcategories': subcategories
    })


# ------------------------
# CUSTOMER
# ------------------------
def customer_details(request):
    return render(request, 'admin_theme/customers/customer_details.html')



# admin_panel/views/category_views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from apps.products.models import Category


# ------------------- LIST -------------------
class CategoryListView(View):
    template_name = 'admin_theme/categories/category.html'

    def get(self, request):
        categories = Category.objects.filter(parent__isnull=True).prefetch_related('subcategories')
        return render(request, self.template_name, {'categories': categories})


# ------------------- CREATE -------------------
class CategoryCreateView(View):
    template_name = 'admin_theme/categories/category_add.html'

    def get(self, request):
        categories = Category.objects.filter(parent__isnull=True)
        return render(request, self.template_name, {'categories': categories})

    def post(self, request):
        name = request.POST.get('category_name')
        slug = request.POST.get('slug')
        description = request.POST.get('description')
        cat_image = request.FILES.get('cat_image')
        parent_id = request.POST.get('parent')
        parent = Category.objects.get(id=parent_id) if parent_id else None
        is_active = request.POST.get('is_active') == 'on'


        Category.objects.create(
            category_name=name,
            slug=slug,
            description=description,
            cat_image=cat_image,
            parent=parent,
            is_active=is_active
            
        )
        return redirect('admin_category_list')


# ------------------- UPDATE -------------------
class CategoryUpdateView(View):
    template_name = 'admin_theme/categories/category_add.html'  # using same form for simplicity

    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        categories = Category.objects.filter(parent__isnull=True)
        return render(request, self.template_name, {'category': category, 'categories': categories})

    def post(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        category.category_name = request.POST.get('category_name')
        category.slug = request.POST.get('slug')
        category.description = request.POST.get('description')
        category.parent_id = request.POST.get('parent') or None

        if 'cat_image' in request.FILES:
            category.cat_image = request.FILES['cat_image']

        category.save()
        return redirect('admin_category_list')


# ------------------- DELETE -------------------
class CategoryDeleteView(View):
    def post(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        category.delete()
        return redirect('admin_category_list')
