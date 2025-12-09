from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from .models import Account, Address

class AccountCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('email', 'username', 'first_name', 'last_name', 'role')

    def clean_password2(self):
        p1 = self.cleaned_data.get('password1')
        p2 = self.cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords do not match")
        return p2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class AccountChangeForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('email', 'username', 'first_name', 'last_name', 'role', 'is_active', 'is_staff', 'is_admin')

class AccountAdmin(UserAdmin):
    form = AccountChangeForm
    add_form = AccountCreationForm

    list_display = ('email', 'username', 'first_name', 'last_name', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'username', 'first_name', 'last_name', 'password', 'role')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_admin', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name', 'role', 'password1', 'password2', 'is_staff', 'is_active')
        }),
    )
    search_fields = ('email', 'username')
    ordering = ('email',)

admin.site.register(Account, AccountAdmin)

admin.site.register(Address)
