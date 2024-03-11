# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Order
# from .utils import export_order_to_excel
# from telegram_client import send_telegram_message

# @receiver(post_save, sender=Order)
# def order_post_save(sender, instance, created, **kwargs):
#     if created:
#         file_path = export_order_to_excel(instance)
#         message = f"Создан новый заказ: {instance.id}. Подробности в приложенном файле."
#         send_telegram_message(message, file_path)
