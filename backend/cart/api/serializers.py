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
    total_cost = serializers.SerializerMethodField()
   
    class Meta:
       model = Cart
       fields = ('id', 'user', 'created_at', 'updated_at', 'items', 'total_items', 'total_cost')
       read_only_fields = ('id', 'user', 'created_at', 'updated_at')
   
    def get_total_cost(self, obj):
        return obj.get_total_cost()
    

