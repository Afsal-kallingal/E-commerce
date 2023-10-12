from rest_framework import serializers
from .models import Account

class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True)
    class Meta:
        model = Account
        fields = ['id', 'email', 'name', 'password','address']
        extra_kwargs = {'password':{'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        account = Account(**validated_data)
        if password is not None:
            account.set_password(password)
        account.save()
        return account

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class PasswordResetSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    otp = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)