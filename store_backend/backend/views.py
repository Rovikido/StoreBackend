from rest_framework import viewsets, mixins, permissions
from .models import ProductType, Product, Cart, CartItem
from rest_framework.exceptions import PermissionDenied
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from rest_framework import permissions

import backend.serializers as serializers
from .models import CustomerUser
from .serializers import UserSerializer



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
        user = self.request.user.id
        return Cart.objects.filter(user=user)

    def perform_create(self, serializer):
        """
        Saves the cart with the current user.
        """
        #TODO: transform os only one cart exists and gets automaticly created
        user_id = self.request.user.id
        user_obj = CustomerUser.objects.get(pk=user_id)
        serializer.save(user=user_obj)


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
        user = self.request.user.id
        return CartItem.objects.filter(cart__user=user)

    def perform_create(self, serializer):
        """
        Saves the cart item with a check to ensure the cart belongs to the current user.
        """
        cart = serializer.validated_data['cart']
        if cart.user.id != self.request.user.id:
            raise PermissionDenied("You do not have permission to add items to this cart.")
        serializer.save()


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomerUser.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['create', 'login', 'register']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        return CustomerUser.objects.filter(id=self.request.user.id)

    @action(detail=False, methods=['post'], url_path='register')
    def register(self, request):
        serializer = serializers.UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'user': UserSerializer(user).data,
                'token': token.key
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request):
        serializer = serializers.UserLoginSerializer(data=request.data)
        
        if serializer.is_valid():
            print(serializer.data)
            username = serializer.data.get('username')
            password = serializer.data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                token, _ = Token.objects.get_or_create(user=user)
                return Response({
                    'user': UserSerializer(user).data,
                    'token': token.key
                }, status=status.HTTP_200_OK)
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
