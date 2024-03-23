from rest_framework.views import APIView, Response, status
from rest_framework import generics
from .models import Basket
from basket.serializers import BasketListSerializer, BasketDetailSerializer
# Create your views here.


class BasketListView(generics.ListAPIView):
    queryset = Basket.objects.all()
    serializer_class = BasketListSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(user=request.user)
        serializer = BasketListSerializer(queryset, many=True)
        return Response(serializer.data)


class BasketDetailView(generics.RetrieveAPIView):
    queryset = Basket.objects.all()
    serializer_class = BasketDetailSerializer






