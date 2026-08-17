from apps.orders.models import Order
from core.exceptions import ApplicationError


def get_user_orders(*, user):
    return Order.objects.filter(user=user).prefetch_related("items").order_by("-created_at")


def get_order_detail(*, order_id, requesting_user):
    order = Order.objects.prefetch_related("items").get(id=order_id)
    if order.user != requesting_user and not requesting_user.is_staff:
        raise ApplicationError("Sizda bu buyurtmani ko'rish huquqi yo'q", status_code=403)
    return order