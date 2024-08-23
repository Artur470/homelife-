from django.db import models
from django.contrib.auth.models import User
from product.models import Product
from django.conf import settings
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.mail import send_mail


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    total_price = models.FloatField(default=0)

    def __str__(self):
        return str(self.user.first_name) + " " + str(self.total_price)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    promotion = models.FloatField(blank=True, null=True)
    isOrder = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return str(self.user.first_name) + " " + str(self.product.title)


@receiver(pre_save, sender=CartItem)
def correct_price(sender, instance, **kwargs):
    product = instance.product
    quantity = instance.quantity
    price_of_product = float(product.price)

    if instance.promotion is not None and instance.promotion > 0:
        # Применяем скидку, если она существует и больше нуля
        discount_percentage = instance.promotion
        discounted_price = price_of_product * (1 - discount_percentage / 100)
        instance.price = quantity * discounted_price
    else:
        # Без промоакции
        instance.price = quantity * price_of_product


#order
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    total_price = models.FloatField(default=0)
    ordered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order {self.id} by {self.user.email}'

    def send_order_email(self):
        subject = 'Новый заказ!'
        message = f'Номер заказа: {self.id}\n' \
                  f'Email: {self.user.email}\n' \
                  f'Имя пользователя: {self.user.first_name} {self.user.last_name}\n' \
                  f'Номер телефона: {self.user.number}\n' \
                  f'Окончательная цена: {self.total_price}\n' \
                  f'Дата заказа: {self.ordered_at}\n\n'

        for item in self.cart.cartitem_set.all():
            item_message = f'Данные продукта:\n' \
                           f'Название: {item.product.title}\n' \
                           f'Категория: {item.product.category}\n' \
                           f'Цвет: {item.product.color}\n' \
                           f'Бренд: {item.product.brand}\n' \
                           f'Количество: {item.quantity}\n' \
                           f'Цена: {item.price}\n'

            # Проверяем, есть ли промоакция для текущего CartItem
            if item.promotion:
                item_message += f'Применённая промоакция: {item.promotion}%\n'
            else:
                item_message += 'Промоакция не применялась.\n'

            item_message += '\n'
            message += item_message

        admin_email = 'homelife.site.kg@gmail.com'
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [admin_email])