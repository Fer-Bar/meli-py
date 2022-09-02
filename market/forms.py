from django import forms
from .models import Seller, Product
from django.utils.translation import gettext_lazy as _


    
class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].required = False
        self.fields['brand'].required = False
        if self.instance and self.instance.pk:
            self.fields.pop('product_id', None)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'
            
    class Meta:
        model = Product
        fields = ['seller_fk', 'title' , 'product_id', 'brand', 'ppv', 'brand_discount_allow']
        exclude = ['seller_id', 'original_price', 'base_price', 'discount_ammount',
                   'discount_percent', 'alert']
        labels = {
            'seller_fk': _('Vendedor'),
            'product_id': _('ProductID'),
            'ppv': _('PPV'),
            'title': _('Nombre del Producto'),
            'brand': _('Marca del Producto'),
            'brand_discount_allow': _('Descuento Permitido por la Marca(%)')
        }
        
class SellerForm(forms.ModelForm): 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'

    class Meta:
        model = Seller
        fields = "__all__"
        labels = {
                'nickname': _('Nickname del Vendedor o ID de vendedor de MELI'),
                'phone': _('Número de Celular o Teléfono (con extensión)'),
                }        
        