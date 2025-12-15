from django.shortcuts import render
from apps.products.models import Category  # make sure Category model exists


# ------------------------
# DASHBOARD
# ------------------------
def admin_dashboard(request):
    return render(request, 'admin_theme/dashboard.html')

# ------------------------
# SUBCATEGORY
# ------------------------
from django.core.paginator import Paginator

def admin_subcategory_list(request, category_id):
    # fetch the parent category
    category = get_object_or_404(Category, id=category_id)
    # fetch subcategories
    subcategories = category.subcategories.all().order_by('-id')
    
    # Add pagination
    paginator = Paginator(subcategories, 4)  # 8 subcategories per page
    page = request.GET.get('page')
    subcategories = paginator.get_page(page)

    return render(request, 'admin_theme/categories/subcategory.html', {
        'category': category,
        'subcategories': subcategories
    })


# admin_panel/views/category_views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from apps.products.models import Category


# ------------------- LIST -------------------
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView
from django.contrib import messages

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

class CategoryListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Category
    template_name = 'admin_theme/categories/category.html'
    context_object_name = 'categories'
    paginate_by = 3
    
    def get_queryset(self):
        return Category.objects.filter(parent__isnull=True).prefetch_related('subcategories').order_by('-id')


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
