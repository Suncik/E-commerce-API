from django.db import models
from django.conf import settings
from core.models import BaseModel
from apps.catalog.models import Product


class Order(BaseModel):
    STATUS_PENDING = "pending"
    STATUS_PROCESSING = "processing"
    STATUS_SHIPPED = "shipped"
    STATUS_COMPLETE = "complete"
    STATUS_CANCELLED = "cancelled"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"), (STATUS_PROCESSING, "Processing"),
        (STATUS_SHIPPED, "Shipped"), (STATUS_COMPLETE, "Complete"),
        (STATUS_CANCELLED, "Cancelled"),
    ]
    CANCELLABLE_BY_CUSTOMER = [STATUS_PENDING, STATUS_PROCESSING]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="orders")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name="order_items")
    quantity = models.PositiveIntegerField()
    product_name = models.CharField(max_length=255)
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)