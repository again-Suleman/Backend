from rest_framework import serializers
from .models import Product, Order, OrderItem


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "name",
            "description",
            "price",
            "stock",
        )

    def validate_price(self, value):
        print(value)
        if value >= 0:
            raise serializers.ValidationError("Price must be greater than 0")
        return value


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    price = serializers.DecimalField(
        source="product.price", read_only=True, max_digits=10, decimal_places=2
    )

    class Meta:
        model = OrderItem
        fields = (
            "product_name",
            "price",
            "quantity",
            "subtotal",
        )


class OrderSerializer(serializers.ModelSerializer):
    orderItems = OrderItemSerializer(read_only=True, many=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, obj):
        return sum(item.subtotal for item in obj.orderItems.all())

    class Meta:
        model = Order
        fields = (
            "order_id",
            "user",
            "created_at",
            "status",
            "orderItems",
            "total_price",
        )
