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
    try:
        if request.method == 'POST':
            form = HomeSliderForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    slider = form.save()
                    messages.success(request, f'Slider "{slider.title}" created successfully!')
                    return redirect('admin_slider_list')
                except Exception as e:
                    messages.error(request, 'Error saving slider. Please try again.')
            else:
                # Form has validation errors
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f'{field.replace("_", " ").title()}: {error}')
        else:
            form = HomeSliderForm()
        return render(request, 'admin_theme/sliders/form.html', {'form': form, 'title': 'Create Slider'})
    except Exception as e:
        messages.error(request, 'Error loading slider form. Please try again.')
        return redirect('admin_slider_list')

def slider_edit(request, slider_id):
    try:
        slider = get_object_or_404(HomeSlider, id=slider_id)
        if request.method == 'POST':
            form = HomeSliderForm(request.POST, request.FILES, instance=slider)
            if form.is_valid():
                try:
                    updated_slider = form.save()
                    messages.success(request, f'Slider "{updated_slider.title}" updated successfully!')
                    return redirect('admin_slider_list')
                except Exception as e:
                    messages.error(request, 'Error updating slider. Please try again.')
            else:
                # Form has validation errors
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f'{field.replace("_", " ").title()}: {error}')
        else:
            form = HomeSliderForm(instance=slider)
        return render(request, 'admin_theme/sliders/form.html', {'form': form, 'title': 'Edit Slider'})
    except Exception as e:
        messages.error(request, 'Error loading slider. Please try again.')
        return redirect('admin_slider_list')

def slider_delete(request, slider_id):
    try:
        slider = get_object_or_404(HomeSlider, id=slider_id)
        slider_title = slider.title
        slider.delete()
        messages.success(request, f'Slider "{slider_title}" deleted successfully!')
    except Exception as e:
        messages.error(request, 'Error deleting slider. Please try again.')
    return redirect('admin_slider_list')
