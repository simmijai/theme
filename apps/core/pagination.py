from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from urllib.parse import urlencode


class GlobalPaginator:
    """Production-ready global pagination utility"""
    
    DEFAULT_PAGE_SIZE = getattr(settings, 'DEFAULT_PAGE_SIZE', 10)
    MAX_PAGE_SIZE = getattr(settings, 'MAX_PAGE_SIZE', 100)
    
    @classmethod
    def paginate(cls, queryset, request, page_size=None):
        """
        Paginate queryset with production-ready features
        """
        page_size = cls._get_page_size(request, page_size)
        paginator = Paginator(queryset, page_size)
        page = request.GET.get('page', 1)
        
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        
        return {
            'page_obj': page_obj,
            'paginator': paginator,
            'is_paginated': paginator.num_pages > 1,
            'page_range': cls._get_page_range(page_obj),
            'query_params': cls._get_query_params(request)
        }
    
    @classmethod
    def _get_page_size(cls, request, default_size=None):
        """Get page size from request or use default"""
        if default_size:
            return min(default_size, cls.MAX_PAGE_SIZE)
        
        try:
            size = int(request.GET.get('per_page', cls.DEFAULT_PAGE_SIZE))
            return min(max(size, 1), cls.MAX_PAGE_SIZE)
        except (ValueError, TypeError):
            return cls.DEFAULT_PAGE_SIZE
    
    @classmethod
    def _get_page_range(cls, page_obj):
        """Get smart page range for pagination display"""
        current_page = page_obj.number
        total_pages = page_obj.paginator.num_pages
        
        if total_pages <= 7:
            return range(1, total_pages + 1)
        
        if current_page <= 4:
            return range(1, 8)
        elif current_page > total_pages - 4:
            return range(total_pages - 6, total_pages + 1)
        else:
            return range(current_page - 3, current_page + 4)
    
    @classmethod
    def _get_query_params(cls, request):
        """Get query parameters excluding page for URL building"""
        params = request.GET.copy()
        if 'page' in params:
            del params['page']
        return params.urlencode()


class PaginationMixin:
    """Mixin for class-based views with global pagination"""
    
    paginate_by = None
    paginate_orphans = 0
    
    def get_paginate_by(self, queryset):
        """Get pagination size"""
        return self.paginate_by or GlobalPaginator.DEFAULT_PAGE_SIZE
    
    def paginate_queryset(self, queryset, page_size):
        """Override default pagination with global paginator"""
        pagination_data = GlobalPaginator.paginate(
            queryset, self.request, page_size
        )
        return (
            pagination_data['paginator'],
            pagination_data['page_obj'],
            pagination_data['page_obj'].object_list,
            pagination_data['is_paginated']
        )
    
    def get_context_data(self, **kwargs):
        """Add pagination context"""
        context = super().get_context_data(**kwargs)
        if context.get('is_paginated'):
            pagination_data = GlobalPaginator.paginate(
                self.get_queryset(), self.request, self.get_paginate_by(None)
            )
            context.update({
                'page_range': pagination_data['page_range'],
                'query_params': pagination_data['query_params']
            })
        return context