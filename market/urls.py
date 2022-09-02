from django.urls import path
from market import views

app_name = 'market'
urlpatterns = [
    path("", views.index_page, name='index'),
    path("createseller/", views.create_seller, name='create_seller'),
    path("createproduct/", views.create_product, name='create_product'),
    path("table_view/", views.TableView.as_view(), name='table_view'),
    path("sellers/", views.SellerView.as_view(), name='sellers'),
    path('details/<str:nickname>/', views.item_details, name='details'),
    path('delete_product/<int:product_id>', views.delete_product, name='delete_product'),
    path('update_product/<int:product_id>', views.update_product, name='update_product'),
]