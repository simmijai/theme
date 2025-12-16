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
from apps.admin_panel.forms import CategoryForm


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
        form = CategoryForm()
        categories = Category.objects.filter(parent__isnull=True)
        return render(request, self.template_name, {'form': form, 'categories': categories})

    def post(self, request):
        form = CategoryForm(request.POST, request.FILES)
        categories = Category.objects.filter(parent__isnull=True)
        
        if form.is_valid():
            category = form.save()
            messages.success(request, f'Category "{category.category_name}" created successfully!')
            return redirect('admin_category_list')
        else:
            # Form has validation errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field.replace("_", " ").title()}: {error}')
        
        return render(request, self.template_name, {'form': form, 'categories': categories})


# ------------------- UPDATE -------------------
class CategoryUpdateView(View):
    template_name = 'admin_theme/categories/category_add.html'

    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        form = CategoryForm(instance=category)
        categories = Category.objects.filter(parent__isnull=True)
        return render(request, self.template_name, {'form': form, 'category': category, 'categories': categories})

    def post(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        form = CategoryForm(request.POST, request.FILES, instance=category)
        categories = Category.objects.filter(parent__isnull=True)
        
        if form.is_valid():
            updated_category = form.save()
            messages.success(request, f'Category "{updated_category.category_name}" updated successfully!')
            return redirect('admin_category_list')
        else:
            # Form has validation errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field.replace("_", " ").title()}: {error}')
        
        return render(request, self.template_name, {'form': form, 'category': category, 'categories': categories})


# ------------------- DELETE -------------------
class CategoryDeleteView(View):
    def post(self, request, pk):
        try:
            category = get_object_or_404(Category, pk=pk)
            category_name = category.category_name
            category.delete()
            messages.success(request, f'Category "{category_name}" deleted successfully!')
        except Exception as e:
            messages.error(request, 'Error deleting category. Please try again.')
        return redirect('admin_category_list')
