from rest_framework import serializers
from apps.catalog.models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = ["id", "name", "price", "stock", "description", "category"]


class ProductWriteSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = ["id", "name", "price", "stock", "description", "category"]