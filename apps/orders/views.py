from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.orders import services, selectors
from apps.orders.serializers import OrderSerializer


class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        return selectors.get_user_orders(user=self.request.user)


class OrderDetailView(APIView):
    def get(self, request, order_id):
        order = selectors.get_order_detail(order_id=order_id, requesting_user=request.user)
        return Response(OrderSerializer(order).data)


class CheckoutView(APIView):
    def post(self, request):
        order = services.checkout_cart(user=request.user)
        return Response(OrderSerializer(order).data, status=201)


class CancelOrderView(APIView):
    def post(self, request, order_id):
        order = selectors.get_order_detail(order_id=order_id, requesting_user=request.user)
        order = services.cancel_order(order=order, actor=request.user)
        return Response(OrderSerializer(order).data)