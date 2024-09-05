from rest_framework import viewsets, mixins, permissions
from .models import ProductType, Product, Cart, CartItem
from rest_framework.exceptions import PermissionDenied
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import update_session_auth_hash

import backend.serializers as serializers
from .models import CustomerUser
from .serializers import UserSerializer
from .permissions import IsAdminOrSelf



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
        elif self.action == 'list':
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated(), IsAdminOrSelf()]

    def get_queryset(self):
        if self.request.user.is_staff:
            return CustomerUser.objects.all()
        return CustomerUser.objects.filter(id=self.request.user.id)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer(user, data=request.data, partial=kwargs.get('partial', False))
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

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

    @action(detail=False, methods=['post'], url_path='change-password', permission_classes=[permissions.IsAuthenticated])
    def change_password(self, request):
        user = request.user
        serializer = serializers.ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            update_session_auth_hash(request, user)
            return Response({'status': 'password_changed'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='username')
    def get_username(self, request):
        return Response({'username': request.user.username}, status=status.HTTP_200_OK)
