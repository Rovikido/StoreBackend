import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
import backend.models as models
from rest_framework.authtoken.models import Token
from django.urls import reverse


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(api_client):
    user = User.objects.create_user(username='testuser', password='testpassword')
    api_client.force_authenticate(user=user)
    return user


@pytest.fixture
def customer_user(api_client):
    user = models.CustomerUser.objects.create_user(
        username='testuser', email='testuser@example.com', password='testpassword',
        first_name='Test', last_name='User', delivery_address='123 Test Street'
    )
    api_client.force_authenticate(user=user)
    return user


@pytest.fixture
def product_type():
    return models.ProductType.objects.create(name='Electronics')


@pytest.fixture
def product(product_type):
    return models.Product.objects.create(
        name='Laptop',
        description='A powerful laptop',
        type=product_type,
        price=1000,
        ammount=10
    )


@pytest.fixture
def cart(customer_user):
    return models.Cart.objects.create(user=customer_user)


@pytest.fixture
def cart_item(cart, product):
    return models.CartItem.objects.create(cart=cart, product=product, ammount=1)


@pytest.mark.django_db
class TestProductTypeViewSet:
    def test_list_product_types(self, api_client):
        url = reverse('ProductTypes-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_create_product_type(self, api_client):
        url = reverse('ProductTypes-list')
        data = {'name': 'Furniture'}
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert models.ProductType.objects.count() == 1

    def test_retrieve_product_type(self, api_client, product_type):
        url = reverse('ProductTypes-detail', args=[product_type.id])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_update_product_type(self, api_client, product_type):
        url = reverse('ProductTypes-detail', args=[product_type.id])
        data = {'name': 'Updated Electronics'}
        response = api_client.patch(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        product_type.refresh_from_db()
        assert product_type.name == 'Updated Electronics'

    def test_delete_product_type(self, api_client, product_type):
        url = reverse('ProductTypes-detail', args=[product_type.id])
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert models.ProductType.objects.count() == 0


@pytest.mark.django_db
class TestProductViewSet:
    def test_list_products(self, api_client):
        url = reverse('Products-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_create_product(self, api_client, product_type):
        url = reverse('Products-list')
        data = {
            'name': 'Tablet',
            'description': 'A new tablet',
            'type': product_type.id,
            'price': 500,
            'ammount': 5
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert models.Product.objects.count() == 1

    def test_retrieve_product(self, api_client, product):
        url = reverse('Products-detail', args=[product.id])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_update_product(self, api_client, product):
        url = reverse('Products-detail', args=[product.id])
        data = {'price': 900}
        response = api_client.patch(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        product.refresh_from_db()
        assert product.price == 900

    def test_delete_product(self, api_client, product):
        url = reverse('Products-detail', args=[product.id])
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert models.Product.objects.count() == 0


@pytest.mark.django_db
class TestCartViewSet:
    def test_list_carts(self, api_client, customer_user, cart):
        url = reverse('Cart-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data[0]['user'] == customer_user.id

    def test_create_cart(self, api_client, customer_user):
        url = reverse('Cart-list')
        data = {'user': customer_user.id}
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert models.Cart.objects.count() == 1
        assert models.Cart.objects.latest('id').user == customer_user

    def test_retrieve_cart(self, api_client, cart):
        url = reverse('Cart-detail', args=[cart.id])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['user'] == cart.user.id

    def test_update_cart(self, api_client, cart):
        url = reverse('Cart-detail', args=[cart.id])
        data = {'user': cart.user.id}
        response = api_client.patch(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK

    def test_delete_cart(self, api_client, cart):
        url = reverse('Cart-detail', args=[cart.id])
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert models.Cart.objects.count() == 0


@pytest.mark.django_db
class TestCartItemViewSet:  
    def test_list_cart_items(self, api_client, customer_user, cart, cart_item):
        url = reverse('CartItems-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data[0]['cart'] == cart.id

    def test_create_cart_item(self, api_client, customer_user, cart, product):
        url = reverse('CartItems-list')
        data = {
            'cart': cart.id,
            'product': product.id,
            'ammount': 2
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert models.CartItem.objects.count() == 1

    def test_retrieve_cart_item(self, api_client, cart_item):
        url = reverse('CartItems-detail', args=[cart_item.id])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_update_cart_item(self, api_client, cart_item):
        url = reverse('CartItems-detail', args=[cart_item.id])
        data = {'ammount': 3}
        response = api_client.patch(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        cart_item.refresh_from_db()
        assert cart_item.ammount == 3

    def test_delete_cart_item(self, api_client, cart_item):
        url = reverse('CartItems-detail', args=[cart_item.id])
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert models.CartItem.objects.count() == 0


@pytest.mark.django_db
class TestUserViewSetGeneral:
    def test_create_user(self, api_client, customer_user):
        url = reverse('User-list')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword',
            'first_name': 'New',
            'last_name': 'User',
            'delivery_address': '456 New Address'
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == 201
        assert models.CustomerUser.objects.count() == 2
        assert models.CustomerUser.objects.get(username='newuser').email == 'newuser@example.com'

    def test_retrieve_user(self, api_client, customer_user):
        api_client.force_authenticate(user=customer_user)
        url = reverse('User-detail', args=[customer_user.id])
        response = api_client.get(url)
        assert response.status_code == 200
        assert response.data['username'] == customer_user.username

    def test_update_user(self, api_client, customer_user):
        api_client.force_authenticate(user=customer_user)
        url = reverse('User-detail', args=[customer_user.id])
        data = {
            'first_name': 'Updated',
            'last_name': 'User',
            'delivery_address': '789 Updated Address'
        }
        response = api_client.patch(url, data, format='json')
        assert response.status_code == 200
        customer_user.refresh_from_db()
        assert customer_user.first_name == 'Updated'
        assert customer_user.delivery_address == '789 Updated Address'

    def test_delete_user(self, api_client, customer_user):
        api_client.force_authenticate(user=customer_user)
        url = reverse('User-detail', args=[customer_user.id])
        response = api_client.delete(url)
        assert response.status_code == 204
        assert models.CustomerUser.objects.count() == 0


@pytest.mark.django_db
class TestUserViewSetAuth:
    def test_register(self, api_client):
        url = reverse('User-register')
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User',
            'delivery_address': '123 Test St'
        }
        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED

        user = models.CustomerUser.objects.get(email='testuser@example.com')
        assert user.username == 'testuser'
        assert user.first_name == 'Test'
        assert user.last_name == 'User'
        assert user.delivery_address == '123 Test St'

    def test_update_password(self, api_client, customer_user):
        api_client.force_authenticate(user=customer_user)
        url = reverse('User-change-password')
        data = {'old_password': 'testpassword', 'new_password': 'newpassword', 'confirm_new_password': 'newpassword'}
        response = api_client.post(url, data, format='json')
        assert response.status_code == 200

        api_client.logout()
        login_response = api_client.post(reverse('User-login'), {'username': customer_user.username, 'password': 'newpassword'} , format='json')
        assert login_response.status_code == 200

    def test_login(self, api_client, customer_user):
        url = reverse('User-login')
        data = {
            'username': customer_user.username,
            'password': 'testpassword'
        }
        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK

        response_data = response.json()
        assert 'token' in response_data
        assert response_data['user']['username'] == customer_user.username