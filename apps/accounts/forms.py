from django import forms
from .models import Account
from django.core.exceptions import ValidationError


# class RegisterForm(forms.ModelForm):
#     password = forms.CharField(
#         widget=forms.PasswordInput,
#         min_length=8,
#         error_messages={"min_length": "Password must be at least 8 characters."}        
#         )
#     confirm_password = forms.CharField(widget=forms.PasswordInput)

#     class Meta:
#         model = Account
#         fields = ['first_name', 'last_name', 'username', 'email', 'password']
        
#     # ❗ Validate email is unique
#     def clean_email(self):
#         email = self.cleaned_data.get("email")
#         if Account.objects.filter(email=email).exists():
#             raise ValidationError("Email is already registered.")
#         return email


#     # ❗ Validate username rules
#     def clean_username(self):
#         username = self.cleaned_data.get("username")
#         if not re.match(r'^[a-zA-Z0-9_.-]+$', username):
#             raise ValidationError("Username can contain letters, numbers, dots, hyphens, and underscores only.")
#         return username

#     # ❗ Validate names (no symbols)
#     def clean_first_name(self):
#         value = self.cleaned_data.get("first_name")
#         if not value.isalpha():
#             raise ValidationError("First name should contain only letters.")
#         return value

#     def clean_last_name(self):
#         value = self.cleaned_data.get("last_name")
#         if not value.isalpha():
#             raise ValidationError("Last name should contain only letters.")
#         return value

#     # ❗ Validate passwords
#     def clean(self):
#         cleaned_data = super().clean()
#         password = cleaned_data.get("password")
#         confirm_password = cleaned_data.get("confirm_password")

#         if password != confirm_password:
#             raise ValidationError("Passwords do not match.")

#         if password and not re.search(r'[A-Z]', password):
#             raise ValidationError("Password must contain at least one uppercase letter.")
#         if password and not re.search(r'[0-9]', password):
#             raise ValidationError("Password must contain at least one number.")
#         return cleaned_data

from django import forms
from .models import Address

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            'first_name', 'last_name', 'phone', 'address_line1', 
            'address_line2','near_by_landmark', 'city', 'state', 'country', 'postal_code'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address_line1': forms.TextInput(attrs={'class': 'form-control'}),
            'address_line2': forms.TextInput(attrs={'class': 'form-control'}),
            'near_by_landmark': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
        } 
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        if not phone.isdigit():
            raise forms.ValidationError("Phone must contain only digits.")

        if len(phone) < 7 or len(phone) > 15:
            raise forms.ValidationError("Enter a valid phone number.")

        if phone == "0000000000":
            raise forms.ValidationError("Invalid phone number.")

        return phone

