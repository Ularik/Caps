from rest_framework import serializers
from .models import Brand, Image, Product, Storage, Favorite, Poster


class ImageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('file', 'is_main')


class BrandListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ('title', 'logo')


class ProductListSerializer(serializers.ModelSerializer):
    images = ImageListSerializer(many=True)
    brands = BrandListSerializer(many=True)

    class Meta:
        model = Product
        fields = ('images', 'title', 'brands', 'price', 'discount')


class ProductCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    images = ImageListSerializer(many=True)

    class Meta:
        model = Product
        fields = ('user', 'title', 'brands', 'color', 'category', 'images', 'description', 'size', 'price', 'discount')


class StorageListSerializer(serializers.ModelSerializer):
    product = ProductListSerializer()

    class Meta:
        model = Storage
        fields = ('id', 'product')


class FavoriteCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Favorite
        fields = ('user', 'product')

    def create(self, validated_data):
        favorite = Favorite(**validated_data)

        favorite.save()
        return favorite


class FavoriteListSerializer(serializers.ModelSerializer):
    storage = StorageListSerializer()

    class Meta:
        model = Favorite
        fields = ('id', 'storage')


class PosterListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poster
        fields = '__all__'


class StorageCreateUpdateSerializer(serializers.ModelSerializer):
    product = ProductCreateSerializer()

    class Meta:
        model = Storage
        fields = ('product', 'quantity', 'status')


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('title', 'brands', 'size', 'color', 'description')


class ProductForBasketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('title', 'price')
