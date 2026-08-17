from django.db import transaction
from django.db.models import F
from core.exceptions import ApplicationError
from apps.cart.models import Cart
from apps.catalog.models import Product
from apps.orders.models import Order, OrderItem


@transaction.atomic
def checkout_cart(*, user):
    cart = Cart.objects.get(user=user)
    cart_items = cart.items.select_related("product").all()

    if not cart_items:
        raise ApplicationError("Savat bo'sh")

    for item in cart_items:
        updated = Product.objects.filter(
            id=item.product_id, stock__gte=item.quantity
        ).update(stock=F("stock") - item.quantity)
        if updated == 0:
            raise ApplicationError(f"{item.product.name} uchun yetarli mahsulot yo'q")

    order = Order.objects.create(user=user, status=Order.STATUS_PENDING)

    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            product_name=item.product.name,
            price_at_purchase=item.product.price,
        )

    cart.items.all().delete()

    return order


def cancel_order(*, order, actor):
    is_owner = order.user == actor
    is_admin = actor.is_staff

    if not is_owner and not is_admin:
        raise ApplicationError("Sizda bu buyurtmani bekor qilish huquqi yo'q", status_code=403)

    if is_owner and not is_admin:
        if order.status not in Order.CANCELLABLE_BY_CUSTOMER:
            raise ApplicationError("Bu buyurtmani endi bekor qilib bo'lmaydi")

    order.status = Order.STATUS_CANCELLED
    order.save(update_fields=["status"])
    return order