from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Cart
from order.models import Order
from .serializers import CartSerializer
from order.serializers import OrderSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    # user=request.user
    if request.method == 'POST':
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_cart(request, cart_id):
    try:
        cart_item = Cart.objects.get(pk=cart_id, user=request.user)
    except Cart.DoesNotExist:
        return Response({'message': 'Cart item not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = CartSerializer(cart_item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_from_cart(request, cart_id):
    try:
        cart_item = Cart.objects.get(pk=cart_id, user=request.user)
    except Cart.DoesNotExist:
        return Response({'message': 'Cart item not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    serializer = CartSerializer(cart_items, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def place_order(request):
    if request.method == 'POST':
        # Assuming you want to place an order from the user's cart
        cart_items = Cart.objects.filter(user=request.user)
        # Create orders based on cart items
        order_data = [{'user': request.user.id, 'product': item.product.id, 'quantity': item.quantity} for item in cart_items]

        serializer = OrderSerializer(data=order_data, many=True)
        if serializer.is_valid():
            serializer.save()
            cart_items.delete()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
