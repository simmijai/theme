from .models import Category

def categories_processor(request):
    categories = Category.objects.filter(parent__isnull=True).prefetch_related('subcategories')
    top_categories = categories[:5]       # first 5 categories
    more_categories = categories[5:]      # the rest
    return {
        'top_categories': top_categories,
        'more_categories': more_categories,
    }
    # return {'categories': categories}
