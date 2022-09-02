from calendar import c
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from market.serializers import ItemSerializer
from market.functions import get_product_id, product_details
from rest_framework import status
from django.views import generic
from django.shortcuts import render, redirect, reverse, get_object_or_404
from .forms import SellerForm, ProductForm
from .models import Product, Seller
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@api_view(['GET'])
@renderer_classes([JSONRenderer])   
def item_details(request, nickname):
    item_data = product_details(get_product_id(nickname))
    serializer = ItemSerializer(item_data, many=True).data
    return Response(serializer, status=status.HTTP_200_OK)

def index_page(request):
    return render(request, 'market/index.html', {})

@login_required
def create_seller(request):
	if request.method == "POST":
		seller_form = SellerForm(request.POST)
		if seller_form.is_valid():
			seller_form.save()
			messages.success(request, ('El vendedor fue creado exitosamente!'))
		else:
			messages.error(request, 'Ups! Al parecer hubo un error con el llenado del formulario. Verifique introducir datos válidos.')
		return redirect(reverse("market:index"))
	seller_form = SellerForm()
	return render(request=request, template_name="market/create_seller.html", context={'seller_form':seller_form})


class TableView(generic.ListView):
    template_name = 'market/table.html'
    queryset = Product.objects.all()
    context_object_name = 'items_data'
    
    def dispatch(self, request, *args, **kwargs):
        for obj in self.queryset:
            obj.email_notify()     
        return super().dispatch(request, *args, **kwargs)
    
class SellerView(generic.ListView):
    template_name = 'market/sellers.html'
    context_object_name = 'seller_data'
    queryset = Seller.objects.all()


@login_required
def create_product(request):
	if request.method == "POST":
		product_form = ProductForm(request.POST)
		item_value = product_form['product_id'].value()
		item_title = product_form['title'].value()
		item_brand = product_form['brand'].value()
		item_details = product_details(item_value)
		if item_details and product_form.is_valid():
			product = product_form.save(commit=False)
			product.title = item_details[0]['title'] if item_title is not None else item_title
			product.brand = item_details[0]['brand'] if item_brand is not None else item_brand
			product.sellerid = item_details[0]['seller_id']
			product.base_price = item_details[0]['base_price']
			product.original_price = item_details[0]['original_price']
			product.discount_ammount = item_details[0]['discount_ammount']
			product.discount_percent = item_details[0]['discount_percent']
			product.brand_discount_allow = product_form['brand_discount_allow'].value()
			product.save()
			messages.success(request, ('Su producto fue añadido exitosamente!'))
			return redirect(reverse("market:table_view"))
		else:
			messages.error(request, 'Ups! Hubo un error con sus datos en el formulario, verifique que el product_id sea correcto.')
	product_form = ProductForm()
	return render(request=request, template_name="market/create_product.html", context={'product_form':product_form})
    
@login_required
def update_product(request, product_id):
    obj = get_object_or_404(Product, pk=product_id)
    if request.method == "POST":
        product_form = ProductForm(request.POST or None, instance = obj)
        if product_form.is_valid():
            product_form.save()
            messages.success(request, ('Su producto fue editado exitosamente!'))
            return redirect(reverse("market:table_view"))
        else:
            messages.error(request, 'Ups! Al parecer hubo un error con el llenado del formulario.')
    else:
        product_form = ProductForm(instance=obj)
    return render(request=request, template_name="market/edit_product.html", context={'product_form':product_form})

@login_required
def delete_product(request, product_id):
    obj = get_object_or_404(Product, pk=product_id)
    obj.delete()
    messages.warning(request, "Producto eliminado.")
    return redirect(reverse("market:table_view"))