from django.contrib import admin
from .models import Product, ProductImage, ProductVariant, ProductAttribute, Category

# Inlines
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3
    fields = ('image', 'is_default')

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 2
    fields = ('color', 'size', 'price', 'stock')

class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 2
    fields = ('key', 'value')

# Product admin with inlines
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'sku', 'price', 'stock', 'is_available', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('price', 'stock', 'is_available')
    inlines = [ProductImageInline, ProductVariantInline, ProductAttributeInline]

# Category admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'parent', 'slug')
    prepopulated_fields = {'slug': ('category_name',)}
    list_filter = ('parent',)
    search_fields = ('category_name',)
