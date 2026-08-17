from django.urls import path
from apps.orders import views

urlpatterns = [
    path("orders/", views.OrderListView.as_view(), name="order-list"),
    path("orders/<uuid:order_id>/", views.OrderDetailView.as_view(), name="order-detail"),
    path("orders/checkout/", views.CheckoutView.as_view(), name="order-checkout"),
    path("orders/<uuid:order_id>/cancel/", views.CancelOrderView.as_view(), name="order-cancel"),
]