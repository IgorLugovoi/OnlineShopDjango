import pytest
from django.urls import reverse
from django.test import Client
from main.models import Cloth, ClothCategory


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
def test_ItemListHome_view(client, cloth):
    url = reverse('itemListHome')
    response = client.get(url)

    assert response.status_code == 200
    assert 'clothes' in response.context
    assert len(response.context['clothes']) == 1
    assert response.context['clothes'][0] == cloth
    assert 'ItemList.html' in [
        template.name for template in response.templates]