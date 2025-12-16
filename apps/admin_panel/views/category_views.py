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
from django.db.models import Q
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
        queryset = Category.objects.filter(parent__isnull=True).prefetch_related('subcategories')
        
        # Search by category name
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(category_name__icontains=search)
        
        # Filter by active status
        status = self.request.GET.get('status')
        if status == 'active':
            queryset = queryset.filter(is_active=True)
        elif status == 'inactive':
            queryset = queryset.filter(is_active=False)
        
        return queryset.order_by('-id')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        context['status'] = self.request.GET.get('status', '')
        return context


# ------------------- CREATE -------------------
class CategoryCreateView(View):
    template_name = 'admin_theme/categories/category_add.html'

    def get(self, request):
        categories = Category.objects.filter(parent__isnull=True)
        return render(request, self.template_name, {'categories': categories})

    def post(self, request):
        name = request.POST.get('category_name', '').strip()
        slug = request.POST.get('slug', '').strip()
        description = request.POST.get('description', '').strip()
        cat_image = request.FILES.get('cat_image')
        parent_id = request.POST.get('parent')
        
        # Validate required fields
        if not name:
            messages.error(request, 'Category name is required.')
            return redirect('admin_category_create')
        
        parent = get_object_or_404(Category, id=parent_id) if parent_id else None
        is_active = request.POST.get('is_active') == 'on'

        Category.objects.create(
            category_name=name,
            slug=slug,
            description=description,
            cat_image=cat_image,
            parent=parent,
            is_active=is_active
        )
        messages.success(request, f'Category "{name}" created successfully!')
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
        name = request.POST.get('category_name', '').strip()
        
        # Validate required fields
        if not name:
            messages.error(request, 'Category name is required.')
            return redirect('admin_category_update', pk=pk)
        
        category.category_name = name
        category.slug = request.POST.get('slug', '').strip()
        category.description = request.POST.get('description', '').strip()
        parent_id = request.POST.get('parent')
        category.parent = get_object_or_404(Category, id=parent_id) if parent_id else None

        if 'cat_image' in request.FILES:
            category.cat_image = request.FILES['cat_image']

        category.save()
        messages.success(request, f'Category "{name}" updated successfully!')
        return redirect('admin_category_list')


# ------------------- DELETE -------------------
class CategoryDeleteView(View):
    def post(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        category.delete()
        return redirect('admin_category_list')
