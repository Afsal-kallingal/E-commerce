from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Payment
import stripe  # Assuming you are using Stripe as the payment gateway

stripe.api_key = 'YOUR_STRIPE_SECRET_KEY'

@api_view(['POST'])
def process_payment(request):
    order_id = request.data.get('order_id')
    amount = request.data.get('amount')
    payment_method = request.data.get('payment_method')
    user = request.user  # Assuming user is authenticated

    try:
        # Create a charge using the Stripe API
        charge = stripe.Charge.create(
            amount=int(float(amount) * 100),  # Amount in cents
            currency='inr',
            source=request.data.get('stripe_token'),  # Token generated by Stripe.js
            description=f'Payment for Order #{order_id}',
        )

        # If the payment is successful, create a Payment record in your database
        Payment.objects.create(
            user=user,
            order_id=order_id,
            amount=amount,
            payment_method=payment_method,
        )

        return Response({'message': 'Payment successful'}, status=status.HTTP_201_CREATED)
    except stripe.error.CardError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': 'An error occurred while processing your payment.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
