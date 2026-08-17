import pytest
from rest_framework.test import APIClient
from apps.catalog.tests.factories import UserFactory, AdminUserFactory, ProductFactory, CategoryFactory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_anyone_authenticated_can_list_products(api_client):
    user = UserFactory()
    ProductFactory.create_batch(3)

    api_client.force_authenticate(user=user)
    response = api_client.get("/api/v1/products/")

    assert response.status_code == 200
    assert len(response.data) == 3


@pytest.mark.django_db
def test_unauthenticated_user_cannot_list_products(api_client):
    ProductFactory.create_batch(2)

    response = api_client.get("/api/v1/products/")

    assert response.status_code == 401


@pytest.mark.django_db
def test_regular_user_cannot_create_product(api_client):
    user = UserFactory()
    category = CategoryFactory()

    api_client.force_authenticate(user=user)
    response = api_client.post("/api/v1/products/", {
        "name": "Yangi mahsulot",
        "price": "5000",
        "stock": 10,
        "category": str(category.id),
    })

    assert response.status_code == 403


@pytest.mark.django_db
def test_admin_can_create_product(api_client):
    admin = AdminUserFactory()
    category = CategoryFactory()

    api_client.force_authenticate(user=admin)
    response = api_client.post("/api/v1/products/", {
        "name": "Yangi mahsulot",
        "price": "5000",
        "stock": 10,
        "category": str(category.id),
    })

    assert response.status_code == 201
    assert response.data["name"] == "Yangi mahsulot"


@pytest.mark.django_db
def test_admin_can_update_product(api_client):
    admin = AdminUserFactory()
    product = ProductFactory(stock=10)

    api_client.force_authenticate(user=admin)
    response = api_client.patch(f"/api/v1/products/{product.id}/", {"stock": 50})

    assert response.status_code == 200
    product.refresh_from_db()
    assert product.stock == 50


@pytest.mark.django_db
def test_regular_user_cannot_delete_product(api_client):
    user = UserFactory()
    product = ProductFactory()

    api_client.force_authenticate(user=user)
    response = api_client.delete(f"/api/v1/products/{product.id}/")

    assert response.status_code == 403


@pytest.mark.django_db
def test_admin_can_delete_product(api_client):
    admin = AdminUserFactory()
    product = ProductFactory()

    api_client.force_authenticate(user=admin)
    response = api_client.delete(f"/api/v1/products/{product.id}/")

    assert response.status_code == 204