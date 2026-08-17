import pytest
from core.exceptions import ApplicationError
from apps.orders import services
from apps.orders.tests.factories import CartFactory, CartItemFactory, ProductFactory


@pytest.mark.django_db
def test_checkout_cart_success():
    cart_item = CartItemFactory(quantity=2)
    product = cart_item.product
    product.stock = 10
    product.save()

    order = services.checkout_cart(user=cart_item.cart.user)

    assert order.status == "pending"
    assert order.items.count() == 1

    order_item = order.items.first()
    assert order_item.price_at_purchase == product.price
    assert order_item.product_name == product.name
    assert order_item.quantity == 2

    product.refresh_from_db()
    assert product.stock == 8  

    assert cart_item.cart.items.count() == 0


@pytest.mark.django_db
def test_checkout_cart_fails_when_stock_insufficient():
    product = ProductFactory(stock=1)
    cart_item = CartItemFactory(product=product, quantity=5)

    with pytest.raises(ApplicationError):
        services.checkout_cart(user=cart_item.cart.user)

    product.refresh_from_db()
    assert product.stock == 1  


@pytest.mark.django_db
def test_checkout_cart_fails_when_cart_empty():
    cart = CartFactory()

    with pytest.raises(ApplicationError):
        services.checkout_cart(user=cart.user)