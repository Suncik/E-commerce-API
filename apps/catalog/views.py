from rest_framework import generics
from apps.catalog.serializers import ProductSerializer, ProductWriteSerializer
from apps.catalog import selectors
from core.permissions import IsAdminOrReadOnly


class ProductListView(generics.ListCreateAPIView):
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        return selectors.get_product_list()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ProductWriteSerializer
        return ProductSerializer


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        return selectors.get_product_list()

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return ProductWriteSerializer
        return ProductSerializer