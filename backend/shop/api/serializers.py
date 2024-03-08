from rest_framework import serializers
from shop.models import Category, Product, ProductImage
from rest_framework.reverse import reverse



class ProductImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ProductImage
        fields = ['image']


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    product_url = serializers.SerializerMethodField()
    add_to_cart_url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['category', 'name', 'product_url',  'add_to_cart_url', 'slug', 'description', 'characteristics', 'price', 'stock', 'available', 'created', 'updated', 'images']
        
    def get_product_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(
            reverse('products-product_detail', kwargs={'slug': obj.slug})
        )
    
    def get_add_to_cart_url(self, obj):
        request = self.context.get('request')
        if request is not None:
            return request.build_absolute_uri(
                reverse('products-add_to_cart', kwargs={'pk': obj.pk})  
            )
        return None

class CategorySerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='category-detail', read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'parent', 'url']


class CategoryDetailSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    children = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'parent', 'children', 'characteristics_template', 'products']


