from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from api.products.serializes import ProductRetrieveSerializer,\
     ProductSerializer
from products.models import Product


class ProductsViewList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]


class ProductsViewRetrieve(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductRetrieveSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

