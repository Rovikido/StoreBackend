from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductTypeViewSet, ProductViewSet, CartViewSet, CartItemViewSet, UserViewSet


router = DefaultRouter()
router.register(r'product-types', ProductTypeViewSet, basename='ProductTypes')
router.register(r'products', ProductViewSet, basename='Products')
router.register(r'cart', CartViewSet, basename='Cart')
router.register(r'cart-items', CartItemViewSet, basename='CartItems')
router.register(r'user', UserViewSet, basename='User')
