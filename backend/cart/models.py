from django.db import models
from django.conf import settings
from shop.models import Product  

class Cart(models.Model):
    """
    Модель представляет корзину пользователя.

    Attributes:
        user (ForeignKey): Ссылка на пользователя, которому принадлежит корзина.
        created_at (DateTimeField): Дата и время создания корзины.
        updated_at (DateTimeField): Дата и время последнего обновления корзины.

    Methods:
        get_total_cost(): Метод для вычисления общей стоимости всех товаров в корзине.
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_total_cost(self):
        return sum(item.quantity * item.product.price for item in self.items.all())



class CartItem(models.Model):
    """
    Модель представляет отдельный товар в корзине.

    Attributes:
        cart (ForeignKey): Ссылка на корзину, к которой относится товар.
        product (ForeignKey): Ссылка на продукт, который является товаром в корзине.
        quantity (PositiveIntegerField): Количество данного товара в корзине.
        added_at (DateTimeField): Дата и время добавления товара в корзину.
    """
    
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

