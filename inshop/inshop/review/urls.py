from django.urls import path
from . import views

urlpatterns = [
    path('create-review/', views.create_review, name='create_review'),
    path('update-review/<int:review_id>/', views.update_review, name='update_review'),
    path('delete-review/<int:review_id>/', views.delete_review, name='delete_review'),
    path('list-reviews/<int:product_id>/', views.list_reviews, name='list_reviews'),
]