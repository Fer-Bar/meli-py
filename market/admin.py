from django.contrib import admin
from .models import Seller, Product
from django import forms
from phonenumber_field.widgets import PhoneNumberPrefixWidget


class ProductInline(admin.StackedInline):
    model = Product
    extra = 1
class SellerForm(forms.ModelForm):
    class Meta:
        widgets = {
            'phone': PhoneNumberPrefixWidget(initial='ARG'),
        }

@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ('nickname', 'email', 'phone')
    form = SellerForm
    inlines = [ProductInline]

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Product._meta.get_fields()]