from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from apps.store.models import HomeSlider
from apps.admin_panel.forms import HomeSliderForm

def slider_list(request):
    sliders = HomeSlider.objects.all().order_by('-id')
    
    # Pagination
    paginator = Paginator(sliders, 10)
    page = request.GET.get('page')
    sliders = paginator.get_page(page)
    
    return render(request, 'admin_theme/sliders/list.html', {
        'sliders': sliders, 
        'is_paginated': sliders.has_other_pages, 
        'page_obj': sliders
    })

def slider_create(request):
    if request.method == 'POST':
        form = HomeSliderForm(request.POST, request.FILES)
        if form.is_valid():
            slider = form.save()
            messages.success(request, f'Slider "{slider.title}" created successfully!')
            return redirect('admin_slider_list')
        else:
            # Form has validation errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field.replace("_", " ").title()}: {error}')
    else:
        form = HomeSliderForm()
    return render(request, 'admin_theme/sliders/form.html', {'form': form, 'title': 'Create Slider'})

def slider_edit(request, slider_id):
    slider = get_object_or_404(HomeSlider, id=slider_id)
    if request.method == 'POST':
        form = HomeSliderForm(request.POST, request.FILES, instance=slider)
        if form.is_valid():
            updated_slider = form.save()
            messages.success(request, f'Slider "{updated_slider.title}" updated successfully!')
            return redirect('admin_slider_list')
        else:
            # Form has validation errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field.replace("_", " ").title()}: {error}')
    else:
        form = HomeSliderForm(instance=slider)
    return render(request, 'admin_theme/sliders/form.html', {'form': form, 'title': 'Edit Slider'})

def slider_delete(request, slider_id):
    slider = get_object_or_404(HomeSlider, id=slider_id)
    slider.delete()
    return redirect('admin_slider_list')
