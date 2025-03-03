from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

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


class UserOrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related(
        "orderItems__product",
    ).all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # It will have the request object containing the authenticated user
        user = self.request.user
        queryset = super().get_queryset()
        return queryset.filter(user=user)
