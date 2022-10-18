from django.contrib import admin
from django import forms
from .models import User, Fuel, Machine, Payment, Creditor


# USERS
class UserForm(forms.ModelForm):
    class Meta:
        widgets = {
            'username': forms.NumberInput(attrs={'class': 'vTextField', 'minlength': 10}),
            'password': forms.PasswordInput(attrs={'class': 'vTextField'}),
        }

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    form = UserForm
    search_fields = ['name', 'username', 'authorisation']
    fields = ['name', 'username', 'password', 'authorisation']
    list_display = ['name', 'username',  'authorisation']
    list_per_page = 10

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(is_superuser=False)


# FUELS

class FuelForm(forms.ModelForm):
    class Meta:
        widgets = {
            'price': forms.NumberInput(attrs={'class': 'vTextField'}),
        }


@admin.register(Fuel)
class FuelAdmin(admin.ModelAdmin):
    form = FuelForm
    search_fields = ['type', 'price']
    list_display = ['type', 'price']
    list_per_page = 10


# PAYMENTS
class PaymentForm(forms.ModelForm):
    class Meta:
        widgets = {
            'allowed_subcategory': forms.CheckboxInput(attrs={'style':'border:none; outline:none; height:14px; width:14px;'})
        }


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    form = PaymentForm
    search_fields = ['mode']
    list_display = ['mode', 'allowed_subcategory']
    list_per_page = 10


# MACHINES
class MachineForm(forms.ModelForm):
    class Meta:
        widgets = {
            'fuel': forms.Select(attrs={'class': 'vTextField'}),
            'reading': forms.NumberInput(attrs={'class': 'vTextField'}),
        }


@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    form = MachineForm
    search_fields = ['name', 'fuel', 'reading']
    list_display = ['name', 'fuel', 'reading']
    list_per_page = 10


# CREDITORS
class CreditorForm(forms.ModelForm):
    class Meta:
        widgets = {
            'payment': forms.Select(attrs={'class': 'vTextField'}),
        }


@admin.register(Creditor)
class CreditorAdmin(admin.ModelAdmin):
    form = CreditorForm
    search_fields = ['payment__mode', 'name',
                     'limit_warning', 'limit_stop_credit']
    list_display = ['payment', 'name', 'limit_warning', 'limit_stop_credit']
    list_per_page = 10
