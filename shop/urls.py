from django.urls import path

from . import views


app_name = 'shop'
urlpatterns = [
    path('products/', views.products_view, name='products'),
    path('product/<int:product_id>', views.product_detail, name='product_detail'),
    path('add_to_cart/<int:product_id>', views.add_to_cart, name='add_to_cart'),
]
