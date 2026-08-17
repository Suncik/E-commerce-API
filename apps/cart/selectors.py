from apps.cart.models import Cart


def get_cart_summary(*, user):
    
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart.items.select_related("product").all()