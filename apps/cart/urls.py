from django.urls import path
from apps.cart import views

urlpatterns = [
    path("cart/", views.CartView.as_view(), name="cart-detail"),
    path("cart/add/", views.AddToCartView.as_view(), name="cart-add"),
    path("cart/remove/<uuid:product_id>/", views.RemoveFromCartView.as_view(), name="cart-remove"),
]