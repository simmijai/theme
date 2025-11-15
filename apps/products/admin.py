from django.contrib import admin
from .models import Category
from .models import Product


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'parent', 'slug')
    prepopulated_fields = {'slug': ('category_name',)}  # works in admin UI
    list_filter = ('parent',)
    search_fields = ('category_name',)

admin.site.register(Category, CategoryAdmin)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'is_available', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('price', 'stock', 'is_available')
