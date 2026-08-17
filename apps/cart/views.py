from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.cart import services, selectors
from apps.cart.serializers import CartItemSerializer, AddToCartSerializer


class CartView(generics.ListAPIView):
  
    serializer_class = CartItemSerializer

    def get_queryset(self):
        return selectors.get_cart_summary(user=self.request.user)


class AddToCartView(APIView):
    # SERVICE ishlatadi — chunki bu yozadi (yaratadi/o'zgartiradi)
    def post(self, request):
        serializer = AddToCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart_item = services.add_to_cart(user=request.user, **serializer.validated_data)
        return Response(CartItemSerializer(cart_item).data, status=status.HTTP_201_CREATED)


class RemoveFromCartView(APIView):
    def delete(self, request, product_id):
        services.remove_from_cart(user=request.user, product_id=product_id)
        return Response(status=status.HTTP_204_NO_CONTENT)