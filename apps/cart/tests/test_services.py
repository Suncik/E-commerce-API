import pytest
from core.exceptions import ApplicationError
from apps.cart import services
from apps.cart.tests.factories import CartFactory, ProductFactory


@pytest.mark.django_db
def test_add_to_cart_creates_new_item():
    cart = CartFactory()
    product = ProductFactory(stock=10)

    cart_item = services.add_to_cart(user=cart.user, product_id=product.id, quantity=2)

    assert cart.items.count() == 1
    assert cart_item.quantity == 2
    assert cart_item.product == product


@pytest.mark.django_db
def test_add_to_cart_increments_existing_item():
    cart = CartFactory()
    product = ProductFactory(stock=10)

    services.add_to_cart(user=cart.user, product_id=product.id, quantity=2)
    cart_item = services.add_to_cart(user=cart.user, product_id=product.id, quantity=3)

    assert cart.items.count() == 1          
    assert cart_item.quantity == 5           


@pytest.mark.django_db
def test_add_to_cart_fails_when_stock_insufficient():
    cart = CartFactory()
    product = ProductFactory(stock=1)

    with pytest.raises(ApplicationError):
        services.add_to_cart(user=cart.user, product_id=product.id, quantity=5)

    assert cart.items.count() == 0        


@pytest.mark.django_db
def test_remove_from_cart():
    cart = CartFactory()
    product = ProductFactory(stock=10)
    services.add_to_cart(user=cart.user, product_id=product.id, quantity=1)

    services.remove_from_cart(user=cart.user, product_id=product.id)

    assert cart.items.count() == 0


@pytest.mark.django_db
def test_remove_from_cart_fails_when_item_not_found():
    cart = CartFactory()
    product = ProductFactory(stock=10)  

    with pytest.raises(ApplicationError):
        services.remove_from_cart(user=cart.user, product_id=product.id)