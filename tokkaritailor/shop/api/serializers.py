from rest_framework import serializers
from shop.models import Category, Product, ProductImage


class CategorySerializer(serializers.ModelSerializer):
    children = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'parent', 'children']

class ProductSerializer(serializers.ModelSerializer):
    images = serializers.SlugRelatedField(many=True, read_only=True, slug_field='image.url')
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'description', 'price', 'stock', 'available', 'created', 'updated', 'category', 'category_id', 'images']

class ProductImageSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'created', 'updated', 'product_id']