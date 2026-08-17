from apps.catalog.models import Product


def get_product_list():
    return Product.objects.select_related("category").all()


def get_product_detail(*, product_id):
    return Product.objects.select_related("category").get(id=product_id)