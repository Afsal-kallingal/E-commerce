from django.urls import path
from . import views

urlpatterns = [
    path('add-product/', views.add_product, name='add_product'),
    path('update-product/<int:product_id>/', views.update_product, name='update_product'),
    path('delete-product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('product-detail/<int:product_id>/', views.product_detail, name='product_detail'),
    path('list/', views.product_list, name='product_list'),
    path('product/', views.search_product, name='search_product'),
    path('addoffer/', views.add_offer_category, name='add_offer'),
    path('removeoffer/', views.remove_offer_category, name='remove_offer'),
]
