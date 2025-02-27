from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer
from rest_framework import generics

# Create your views here.


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = "slug"


class OrderListView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related(
        "orderItems__product",
    ).all()
    serializer_class = OrderSerializer
