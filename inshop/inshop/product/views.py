from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import Product
from .serializers import ProductSerializer,ProductOfferAddSerializer,ProductOfferRemoveSerializer
from rest_framework.permissions import AllowAny
from account.permissions import IsAdmin, IsAuthenticated

@api_view(['POST'])
@permission_classes([IsAdmin])
def add_product(request):
    if request.method == 'POST':
        offer= int(request.data.get('offer'))
        amount=int(request.data.get('amount'))
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            if offer:
                serializer.save(amount=amount-(amount*offer/100))
            else:
                serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@permission_classes([AllowAny])
def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)  
    
    return Response(serializer.data,)

@api_view(['PUT'])
@permission_classes([IsAdmin])
def update_product(request,product_id):
    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        return Response({'message': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        offer= int(request.data.get('offer'))
        amount=int(request.data.get('amount'))

            # amount.save()
        if serializer.is_valid():
            if offer:
                serializer.save(amount=amount-(amount*offer/100))
            else:
                serializer.save()



            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAdmin])
def delete_product(request, product_id):
    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        return Response({'message': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def product_detail(request, product_id):
    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        return Response({'message': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
@api_view(['POST'])
@permission_classes([IsAdmin])
def add_offer_category(request):
    serializer = ProductOfferAddSerializer(data=request.data)

    if serializer.is_valid():
        category = serializer.validated_data['category']
        offer = serializer.validated_data.get('offer', 0)
        try:
            products = Product.objects.filter(category=category)
            for product in products:
                amount = product.amount
                if offer:
                    product.amount=amount-(amount*offer/100)
                    product.save()
            return Response({'message': 'offer added successfully'})
        except Product.DoesNotExist:
            return Response({'message': 'Product not found for the given category'}, status=status.HTTP_404_NOT_FOUND)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAdmin])
def remove_offer_category(request):
    serializer = ProductOfferRemoveSerializer(data=request.data)
    if serializer.is_valid():
        category = request.data.get('category')
        products = Product.objects.filter(category=category)
        for product in products:
            product.amount = product.oldamount
            product.save()
        return Response({'message': 'offer removed successfully'})
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
   
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_product(request):
    product_name = request.query_params.get('name')
    products = Product.objects.filter(name__icontains=product_name)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def product_search(request):
#     search_query = request.query_params.get('q', '')
#     products = Product.objects.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))
#     serializer = ProductSerializer(products, many=True)
#     return Response(serializer.data)
