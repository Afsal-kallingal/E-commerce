from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ProductOfferAddSerializer(serializers.Serializer):
    category = serializers.CharField(max_length=255)
    offer = serializers.DecimalField(max_digits=5, decimal_places=2, default=0)

class ProductOfferRemoveSerializer(serializers.Serializer):
    category = serializers.CharField(max_length=255)