from django.db.models import F
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import Response, APIView, status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
    ListCreateAPIView
)
from datetime import datetime, timedelta, time
from basket.models import Basket
from .models import Brand, Product, Storage, Poster, Favorite
from .serializers import (
    StorageListSerializer,
    PosterListSerializer,
    BrandListSerializer,
    StorageCreateUpdateSerializer,
    ProductDetailSerializer,
    ProductForBasketSerializer, FavoriteCreateSerializer,
    FavoriteListSerializer
)
from basket.serializers import BasketCreateSerializer
from .filters import StorageFilter
from random import randint
from collections import deque
from decimal import Decimal


class IndexListView(APIView):

    def get(self, request):
        # requests
        posters = Poster.objects.all()
        brands = Brand.objects.all()
        bestsellers = ProductBestsellersListView.bestseller()
        sales = Storage.objects.filter(product__discount__gt=F('product__price'))

        # serializers
        posters_serializer = PosterListSerializer(posters, many=True)
        brands_serializer = BrandListSerializer(brands, many=True)
        products_serializer = StorageListSerializer(bestsellers, many=True)
        sales_serializer = StorageListSerializer(sales, many=True)

        data = {
            'posters': posters_serializer.data,
            'brands': brands_serializer.data,
            'bestseller': products_serializer.data,
            'sales': sales_serializer.data,
        }

        return Response(data)


class ProductDiscountView(ListAPIView):
    queryset = Storage.objects.filter(product__discount__gt=F('product__price'))
    serializer_class = StorageListSerializer


class ProductBestsellersListView(APIView):
    @staticmethod
    def bestseller():

        baskets = Basket.objects.all()
        bestsellers = deque([], maxlen=10)
        dct = {}
        for basket in baskets:
            dct[basket.storage] = dct.get('baskets.storage', 0) + 1

        arr = sorted(dct, key=lambda x: dct[x])
        for storage in arr:
            bestsellers.append(storage)

        return bestsellers

    def get(self, request):

        bestsellers = self.bestseller()
        products_serializer = StorageListSerializer(bestsellers, many=True)

        return Response(products_serializer.data, status.HTTP_200_OK)


class StorageListView(ListCreateAPIView):
    queryset = Storage.objects.all()
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ['product__title']
    ordering_fields = ['product__price', 'product__created_date']
    filterset_class = StorageFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return StorageListSerializer
        elif self.request.method == 'POST':
            return FavoriteCreateSerializer


class StorageDetailView(RetrieveAPIView):
    queryset = Storage.objects.all()
    serializer_class = StorageListSerializer


class StorageCreateView(CreateAPIView):
    queryset = Storage.objects.all()
    serializer_class = StorageCreateUpdateSerializer


class StorageUpdateView(UpdateAPIView):
    queryset = Storage.objects.all()
    serializer_class = StorageCreateUpdateSerializer


class StorageDeleteView(DestroyAPIView):
    queryset = Storage.objects.all()
    serializer_class = StorageCreateUpdateSerializer


class ProductDetailView(APIView):

    def get(self, request, pk):

        product = Product.objects.get(pk=pk)
        serializer = ProductDetailSerializer(product, context={'request': request})

        return Response(serializer.data, status.HTTP_200_OK)


class ProductForBasketView(APIView):

    def get(self, request, pk):

        product = Product.objects.get(pk=pk)

        serializer = ProductForBasketSerializer(product, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        storage = Storage.objects.get(product=pk)
        quantity = request.data.pop('quantity', 1)

        dispatch_date = datetime.now() + timedelta(hours=4)

        if (datetime.now() + timedelta(hours=4)).time() > time(18):
            dispatch_date = (datetime.now() + timedelta(days=1)).replace(hour=10)


        data = {
            'user': request.user.id,
            'storage': storage.id,
            'quantity': quantity,
            'dispatch_date': dispatch_date,
            'unique_code': randint(1, 999) * randint(1, 999),
            'address': request.user.address,
            'delivery_sum': storage.product.price * Decimal(quantity),
            'status': 3
        }
        serializer = BasketCreateSerializer(data=data, context={'request': request})

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class FavoriteListView(ListAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteListSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(user=request.user)
        serializer = FavoriteListSerializer(queryset, many=True)
        return Response(serializer.data)
