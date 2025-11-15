from django import forms
from apps.products.models import Product, ProductImage
from apps.store.models import HomeSlider


# ✅ Custom widget for selecting multiple files
class MultiFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


# ✅ Main Product Form
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name', 'description', 'price', 'image', 'stock', 'is_available']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Product description', 'rows': 3}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),  # single image
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Stock quantity'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


# ✅ Form for multiple additional images
class ProductImageForm(forms.Form):
    images = forms.FileField(
        required=False,
        widget=MultiFileInput(
            attrs={
                'multiple': True,
                'class': 'form-control',
                'name': 'images',  # important for getlist('images')
            }
        )
    )
    
    

class HomeSliderForm(forms.ModelForm):
    class Meta:
        model = HomeSlider
        fields = ['title', 'subtitle', 'image', 'button_text', 'button_link', 'is_active', 'order']

