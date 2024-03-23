from rest_framework import serializers
from .models import Basket
from product.serializers import StorageListSerializer


class BasketListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Basket
        fields = ('id', 'unique_code', 'created_date', 'dispatch_date', 'status')


class BasketDetailSerializer(serializers.ModelSerializer):
    storage = StorageListSerializer()
    class Meta:
        model = Basket
        fields = ('id', 'storage', 'quantity', 'delivery_sum')


class BasketCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Basket
        fields = ('user', 'storage', 'quantity', 'address', 'unique_code', 'delivery_sum', 'status')