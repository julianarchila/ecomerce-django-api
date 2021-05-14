""" Product views. """

# Django REST Framework
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated, IsAdminUser

# Serializers
from products.serializers import ProductModelSerializer, CreateProductSerializer

# Models
from products.models import Product



class ProductViewSet(ListModelMixin,CreateModelMixin,GenericViewSet):
    """Product view set. """
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        permissions = [IsAuthenticated]
        if self.action == "create":
            permissions.append(IsAdminUser)

        return [p() for p in permissions]

    def create(self, request, *args, **kwargs):
        serializer = CreateProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        data = ProductModelSerializer(product).data
        return Response(data=data, status=status.HTTP_201_CREATED)


    