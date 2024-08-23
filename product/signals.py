from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Product


@receiver(pre_save, sender=Product)
def ensure_single_product_of_the_day(sender, instance, **kwargs):
    if instance.is_product_of_the_day:
        Product.objects.filter(is_product_of_the_day=True).update(is_product_of_the_day=False)
