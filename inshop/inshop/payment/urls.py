# from django.urls import path
# from . import views

# urlpatterns = [
#     path('api/payments/', views.PaymentListCreateView.as_view(), name='payment-list-create'),
#     path('api/payments/<int:pk>/', views.PaymentDetailView.as_view(), name='payment-detail'),
#     path('api/process_payment/', views.ProcessPaymentView.as_view(), name='process-payment'),
#     # Add other URLs as needed
# ]

from django.urls import path
from . import views

urlpatterns = [
    path('process/', views.process_payment, name='process_payment'),
    # Add other URLs as needed
]
