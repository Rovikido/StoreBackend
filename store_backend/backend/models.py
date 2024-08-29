from django.db import models
from django.core.validators import MaxLengthValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser


class CustomerUserManager():
    pass


class CustomerUser(AbstractUser):
    delivery_address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.username


class ProductType(models.Model):
    name = models.CharField(max_length=128, blank=False, validators=[
        MaxLengthValidator(limit_value=128, message='Product type name is too long!')])


class Product(models.Model):
    name = models.CharField(max_length=128, blank=False, validators=[
        MaxLengthValidator(limit_value=128, message='Product name is too long!')])
    description = models.CharField(max_length=4096, blank=True, validators=[
        MaxLengthValidator(limit_value=4096, message='Product description is too long!')])
    type = models.ForeignKey(ProductType, on_delete=models.CASCADE, null=False)
    price = models.IntegerField(blank=False, validators=[
        MinValueValidator(limit_value=0, message='Price cannot be negative!')])
    ammount = models.IntegerField(blank=False, validators=[
        MinValueValidator(limit_value=0, message='Ammount cannot be negative!')])


class Cart(models.Model):
    user = models.ForeignKey(CustomerUser, on_delete=models.CASCADE, null=False)


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False)
    ammount = models.IntegerField(blank=False, validators=[
        MinValueValidator(limit_value=0, message='Ammount cannot be negative!')])
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, blank=False)