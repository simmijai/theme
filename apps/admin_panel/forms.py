from django import forms
from apps.products.models import Product, ProductImage, Category
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
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price', 'step': '0.01', 'min': '0'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Stock quantity', 'min': '0'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name or len(name.strip()) < 3:
            raise forms.ValidationError('Product name must be at least 3 characters long.')
        # Sanitize input
        name = name.strip()
        import re
        name = re.sub(r'\s+', ' ', name)
        # Check for valid characters
        if not re.match(r'^[a-zA-Z0-9\s\-_&.,()]+$', name):
            raise forms.ValidationError('Product name contains invalid characters.')
        return name
    
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise forms.ValidationError('Price must be greater than 0.')
        return price
    
    def clean_stock(self):
        stock = self.cleaned_data.get('stock')
        if stock is not None and stock < 0:
            raise forms.ValidationError('Stock cannot be negative.')
        return stock


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
    
    

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name', 'slug', 'description', 'cat_image', 'parent', 'is_active']
        widgets = {
            'category_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Category name'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'URL slug'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Category description'}),
            'cat_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'parent': forms.Select(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def clean_category_name(self):
        name = self.cleaned_data.get('category_name')
        if not name or len(name.strip()) < 2:
            raise forms.ValidationError('Category name must be at least 2 characters long.')
        # Sanitize input
        name = name.strip()
        # Remove multiple spaces
        import re
        name = re.sub(r'\s+', ' ', name)
        # Check for valid characters (letters, numbers, spaces, hyphens)
        if not re.match(r'^[a-zA-Z0-9\s\-_&]+$', name):
            raise forms.ValidationError('Category name contains invalid characters.')
        return name
    
    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        if slug:
            # Sanitize slug
            import re
            slug = slug.strip().lower()
            slug = re.sub(r'[^a-z0-9\-_]', '-', slug)
            slug = re.sub(r'-+', '-', slug).strip('-')
            # Check for duplicate slug
            if Category.objects.filter(slug=slug).exclude(pk=self.instance.pk if self.instance else None).exists():
                raise forms.ValidationError('This slug already exists. Please choose a different one.')
        return slug

class AdminLoginForm(forms.Form):
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email',
            'required': True
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password',
            'required': True
        })
    )
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError('Email is required.')
        return email.lower().strip()
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password or len(password) < 6:
            raise forms.ValidationError('Password must be at least 6 characters long.')
        return password

class HomeSliderForm(forms.ModelForm):
    class Meta:
        model = HomeSlider
        fields = ['title', 'subtitle', 'image', 'button_text', 'button_link', 'is_active', 'order']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Slider title'}),
            'subtitle': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Slider subtitle'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'button_text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Button text'}),
            'button_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Button URL'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title or len(title.strip()) < 3:
            raise forms.ValidationError('Title must be at least 3 characters long.')
        # Sanitize input
        title = title.strip()
        import re
        title = re.sub(r'\s+', ' ', title)
        # Check for valid characters
        if not re.match(r'^[a-zA-Z0-9\s\-_&.,()!]+$', title):
            raise forms.ValidationError('Title contains invalid characters.')
        return title
    
    def clean_image(self):
        from PIL import Image
        image = self.cleaned_data.get('image')
        if image:
            try:
                img = Image.open(image)
                width, height = img.size
                if width != 1096 or height != 895:
                    raise forms.ValidationError(f'Image must be exactly 1920x600 pixels. Uploaded: {width}x{height}px')
                if image.size > 2 * 1024 * 1024:
                    raise forms.ValidationError('Image file size must be less than 2MB')
            except Exception as e:
                if 'Image must be exactly' in str(e) or 'file size' in str(e):
                    raise
                raise forms.ValidationError('Invalid image file')
        return image
    
    def clean_order(self):
        order = self.cleaned_data.get('order')
        if order is not None and order < 0:
            raise forms.ValidationError('Order must be a positive number.')
        return order

