from django.core.mail import send_mail
from django.conf import settings


def send_order_notification(order):
    subject = f'Новый заказ #{order.id}'
    message = f'Детали заказа:\n\n' \
              f'Заказ ID: {order.id}\n' \
              f'Общая сумма: {order.total_price}\n' \
              f'Дата создания: {order.created_at}\n'
    recipient_list = ['homelife.site.kg@gmail.com']
    send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
