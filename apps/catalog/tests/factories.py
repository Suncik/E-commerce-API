import factory
from django.contrib.auth.models import User
from apps.catalog.models import Category, Product


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    is_staff = False


class AdminUserFactory(UserFactory):
    is_staff = True


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = "Ichimliklar"


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    category = factory.SubFactory(CategoryFactory)
    name = "Test mahsulot"
    price = 10000
    stock = 10