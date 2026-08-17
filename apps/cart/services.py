from core.exceptions import ApplicationError
from apps.cart.models import Cart, CartItem
from apps.catalog.models import Product


def add_to_cart(*, user, product_id, quantity):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        raise ApplicationError("Mahsulot topilmadi", status_code=404)

    if product.stock < quantity:
        raise ApplicationError("Yetarli mahsulot yo'q")

    cart, _ = Cart.objects.get_or_create(user=user)

    
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart, product=product, defaults={"quantity": quantity}
    )
    if not created:
        cart_item.quantity += quantity
        cart_item.save(update_fields=["quantity"])

    return cart_item


def remove_from_cart(*, user, product_id):
    cart = Cart.objects.get(user=user)
    deleted_count, _ = CartItem.objects.filter(cart=cart, product_id=product_id).delete()
    if deleted_count == 0:
        raise ApplicationError("Bu mahsulot savatda topilmadi", status_code=404)