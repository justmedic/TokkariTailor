from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from cart.models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer



class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        serializer.save(user=self.request.user)



class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user_cart = Cart.objects.filter(user=self.request.user)
        return CartItem.objects.filter(cart__in=user_cart)
   

    
    def perform_create(self, serializer):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        product = serializer.validated_data['product']
        quantity = serializer.validated_data['quantity']
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': quantity})
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
            
        serializer.instance = cart_item
   

