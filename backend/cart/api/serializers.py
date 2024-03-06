from rest_framework import serializers
from cart.models import Cart, CartItem
from shop.models import Product

class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    
    class Meta:
        model = CartItem
        fields = ('id', 'product', 'product_name', 'quantity', 'added_at')
        read_only_fields = ('id', 'added_at')

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_items = serializers.SerializerMethodField()
    
    class Meta:
        model = Cart
        fields = ('id', 'user', 'created_at', 'updated_at', 'items', 'total_items')
        read_only_fields = ('id', 'user', 'created_at', 'updated_at')

    def get_total_items(self, obj):
        return sum(item.quantity for item in obj.items.all())
