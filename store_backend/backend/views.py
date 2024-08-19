from rest_framework import viewsets, mixins
from .models import ProductType, Product, Cart, CartItem
from rest_framework.exceptions import PermissionDenied
import backend.serializers as serializers


class ProductTypeViewSet(mixins.CreateModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin,
                         mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    queryset = ProductType.objects.all()
    serializer_class = serializers.ProductTypeSerializer


class ProductViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer


class CartViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    serializer_class = serializers.CartSerializer

    def get_queryset(self):
        """
        Returns the carts that belong to the current user.
        """
        user = self.request.user
        return Cart.objects.filter(user=user)

    def perform_create(self, serializer):
        """
        Saves the cart with the current user.
        """
        #TODO: transform os only one cart exists and gets automaticly created
        serializer.save(user=self.request.user)


class CartItemViewSet(mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    serializer_class = serializers.CartItemSerializer

    def get_queryset(self):
        """
        Returns the cart items that belong to the current user's carts.
        """
        user = self.request.user
        return CartItem.objects.filter(cart__user=user)

    def perform_create(self, serializer):
        """
        Saves the cart item with a check to ensure the cart belongs to the current user.
        """
        cart = serializer.validated_data['cart']
        if cart.user != self.request.user:
            raise PermissionDenied("You do not have permission to add items to this cart.")
        serializer.save()
