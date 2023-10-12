from django.urls import path
from . import views

urlpatterns = [
    path('add-cart/', views.add_to_cart, name='add_to_cart'),
    path('update-cart/<int:cart_id>/', views.update_cart, name='update_cart'),
    path('delete-cart/<int:cart_id>/', views.delete_from_cart, name='delete_from_cart'),
    path('list-cart/', views.list_cart, name='list_cart'),
    path('place-order/', views.place_order, name='place_order'),
]

