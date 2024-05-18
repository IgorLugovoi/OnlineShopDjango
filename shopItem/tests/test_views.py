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
        sort=1,
        photo="media\cloth\Mina_Dress_In_Ivory_wWTq9Ab.jpg"
    )


@pytest.mark.django_db
def test_shop_item_detail_view(client, cloth):
    url = reverse('shop_item_detail', args=[cloth.slug])
    response = client.get(url)
    assert response.status_code == 200
    assert 'cloth' in response.context
    assert 'order_items' in response.context
    assert 'total' in response.context
    assert response.context['cloth'] == cloth


@pytest.mark.django_db
def test_add_to_cart_view(client, cloth):
    url = reverse('add_to_cart', args=[cloth.id])
    response = client.post(url)
    assert response.status_code == 200
    assert 'cart' in client.session
    assert str(cloth.id) in client.session['cart']
    assert client.session['cart'][str(cloth.id)]['quantity'] == 1
    assert float(client.session['cart'][str(cloth.id)]
                 ['total_price']) == cloth.price


@pytest.mark.django_db
def test_clear_cart_view(client):
    url = reverse('clear_cart')
    client.session['cart'] = {'1': {'quantity': 2, 'total_price': '39.98'}}
    client.session.save()
    response = client.post(url)
    assert response.status_code == 200
    assert 'cart' in client.session
    assert client.session['cart'] == {}

@pytest.mark.django_db
def test_order_item_view(client: Client, cloth: Cloth):
    # Set up session data
    session = client.session
    session['cart'] = {
        str(cloth.id): {
            'quantity': 2,
            'total_price': '39.98'
        }
    }
    session.save()

    # Perform the GET request
    url = reverse('order_item')
    response = client.get(url)

    # Debug prints
    print("Response status code:", response.status_code)
    print("Response context:", response.context)
    print("Session data:", client.session['cart'])

    # Assertions
    assert response.status_code == 200
    assert 'order_items' in response.context
    assert 'total' in response.context
    assert len(response.context['order_items']) == 1
    assert response.context['order_items'][0]['cloth'] == cloth
    assert response.context['order_items'][0]['quantity'] == 2
    assert float(response.context['order_items'][0]['total_price']) == 39.98
    assert float(response.context['total']) == 39.98
