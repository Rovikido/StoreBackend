from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

from .models import ProductType, Product, Cart, CartItem, CustomerUser


CustomerUser = get_user_model()


class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = ['id', 'name']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'type', 'price', 'ammount']


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'user']


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'ammount', 'cart']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerUser
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'delivery_address')

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomerUser
        fields = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'delivery_address', 'password')

    def create(self, validated_data):
        user = CustomerUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone_number=validated_data.get('phone_number', ''),
            delivery_address=validated_data.get('delivery_address', ''),
            password=validated_data['password']
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_new_password = serializers.CharField(write_only=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value

    def validate(self, data):
        if data['new_password'] != data['confirm_new_password']:
            raise serializers.ValidationError("New and confirmation passwords do not match.")
        return data
