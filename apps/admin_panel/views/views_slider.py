from django.shortcuts import render, redirect, get_object_or_404
from apps.store.models import HomeSlider
from apps.admin_panel.forms import HomeSliderForm

def slider_list(request):
    sliders = HomeSlider.objects.all()
    return render(request, 'admin_theme/sliders/list.html', {'sliders': sliders})

def slider_create(request):
    if request.method == 'POST':
        form = HomeSliderForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_slider_list')
    else:
        form = HomeSliderForm()
    return render(request, 'admin_theme/sliders/form.html', {'form': form, 'title': 'Create Slider'})

def slider_edit(request, slider_id):
    slider = get_object_or_404(HomeSlider, id=slider_id)
    if request.method == 'POST':
        form = HomeSliderForm(request.POST, request.FILES, instance=slider)
        if form.is_valid():
            form.save()
            return redirect('admin_slider_list')
    else:
        form = HomeSliderForm(instance=slider)
    return render(request, 'admin_theme/sliders/form.html', {'form': form, 'title': 'Edit Slider'})

def slider_delete(request, slider_id):
    slider = get_object_or_404(HomeSlider, id=slider_id)
    slider.delete()
    return redirect('admin_slider_list')
