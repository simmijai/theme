from django.contrib import admin
from .models import Category

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'parent', 'slug')
    prepopulated_fields = {'slug': ('category_name',)}  # works in admin UI
    list_filter = ('parent',)
    search_fields = ('category_name',)

admin.site.register(Category, CategoryAdmin)
