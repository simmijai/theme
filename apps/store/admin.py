from django.contrib import admin
from .models import HomeSlider,Review

@admin.register(HomeSlider)
class HomeSliderAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    
admin.site.register(Review)