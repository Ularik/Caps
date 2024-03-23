from django.db import models
from django.contrib.auth import get_user_model
from product.models import Storage

User = get_user_model()


# Create your models here.
class Basket(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT
    )
    storage = models.ForeignKey(
        Storage,
        on_delete=models.PROTECT
    )
    quantity = models.PositiveIntegerField(default=1)
    address = models.CharField(max_length=123)
    created_date = models.DateTimeField(auto_now_add=True)
    dispatch_date = models.DateTimeField(
        null=True,
        blank=True
    )
    unique_code = models.IntegerField(unique=True)
    delivery_sum = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00
    )
    status = models.PositiveSmallIntegerField(
        choices=(
            (1, 'отправляется'),
            (2, 'доставлено'),
            (3, 'рассматривается')
        )
    )
