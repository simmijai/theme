from .models import Category

def categories_processor(request):
    categories = Category.objects.filter(parent__isnull=True).prefetch_related('subcategories')
    return {'categories': categories}
