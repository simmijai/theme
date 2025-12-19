from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .pagination import PaginationMixin


class BaseAdminView(LoginRequiredMixin, UserPassesTestMixin):
    """Base view for admin functionality"""
    
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser


class BasePaginatedListView(BaseAdminView, PaginationMixin, ListView):
    """Base paginated list view for admin"""
    
    paginate_by = 10
    ordering = ['-id']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_count'] = self.get_queryset().count()
        return context