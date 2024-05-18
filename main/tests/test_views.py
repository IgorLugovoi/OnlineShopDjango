import pytest
from django.urls import reverse
from django.test import Client
from main.models import ClothCategory, Cloth, Order, OrderItem

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def cloth_category():
    return ClothCategory.objects.create(name="Shirts", slug="shirts", is_visible=True, sort=1)

@pytest.fixture
def cloth(cloth_category):
    return Cloth.objects.create(
        name="T-Shirt",
        slug="t-shirt",
        category=cloth_category,
        genre="male",
        color="red",
        size="M",
        brand="BrandA",
        material="cotton",
        price=19.99,
        is_visible=True,
        sort=1
    )

@pytest.mark.django_db
def test_home_view(client, cloth_category):
    url = reverse('home')
    response = client.get(url)
    assert response.status_code == 200
    assert 'categories' in response.context
    assert 'form' in response.context
    assert 'order_items' in response.context
    assert 'total_price' in response.context

@pytest.mark.django_db
def test_view_cart_and_order_post(client, cloth):
    cart = {
        str(cloth.id): {
            'quantity': 2,
            'total_price': '39.98'
        }
    }
    session = client.session
    session['cart'] = cart
    session.save()

    url = reverse('cart_detail')
    form_data = {
        'name': 'John Doe',
        'email': 'john.doe@example.com',
        'phone': '+380509999999',
        'comment': 'Please deliver between 9am and 5pm'
    }
    response = client.post(url, form_data)
    assert response.status_code == 302  # Перевірка, що відбулося перенаправлення
    assert response.url == reverse('home')  # Перевірка, що перенаправлення на головну сторінку

    order = Order.objects.first()
    assert order is not None
    assert order.name == 'John Doe'
    assert order.email == 'john.doe@example.com'
    assert order.phone == '+380509999999'
    assert order.comment == 'Please deliver between 9am and 5pm'
    assert not order.is_processed

    order_item = OrderItem.objects.first()
    assert order_item is not None
    assert order_item.order == order
    assert order_item.cloth == cloth
    assert order_item.quantity == 2
    assert float(order_item.total_price) == 39.98

@pytest.mark.django_db
def test_view_cart_and_order_get(client):
    url = reverse('cart_detail')
    response = client.get(url)
    assert response.status_code == 200
    assert 'form' in response.context
    assert 'order_items' in response.context
