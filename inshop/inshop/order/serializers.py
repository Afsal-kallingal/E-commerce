from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

        extra_kwargs = {
            'user': {'read_only': True},
            }
class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

        extra_kwargs = {
            'user': {'read_only': True},
            'product': {'read_only': True},
            }