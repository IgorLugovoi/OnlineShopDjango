import pytest
from django.core.exceptions import ValidationError
from ..models import ClothCategory, Cloth, Order, OrderItem

@pytest.mark.django_db
def test_cloth_category_creation():
    category = ClothCategory.objects.create(name="Shirts", slug="shirts", is_visible=True, sort=1)
    assert category.name == "Shirts"
    assert category.slug == "shirts"
    assert category.is_visible is True
    assert category.sort == 1

@pytest.mark.django_db
def test_cloth_creation():
    category = ClothCategory.objects.create(name="Shirts", slug="shirts")
    cloth = Cloth.objects.create(
        name="T-Shirt",
        slug="t-shirt",
        category=category,
        genre="male",
        color="red",
        size="M",
        brand="BrandA",
        material="cotton",
        description="A red T-Shirt",
        price=19.99,
        is_visible=True,
        sort=1
    )
    assert cloth.name == "T-Shirt"
    assert cloth.slug == "t-shirt"
    assert cloth.category == category
    assert cloth.genre == "male"
    assert cloth.color == "red"
    assert cloth.size == "M"
    assert cloth.brand == "BrandA"
    assert cloth.material == "cotton"
    assert cloth.description == "A red T-Shirt"
    assert cloth.price == 19.99
    assert cloth.is_visible is True
    assert cloth.sort == 1

@pytest.mark.django_db
def test_order_creation():
    order = Order.objects.create(
        name="John Doe",
        email="john.doe@example.com",
        phone="+380509999999",
        comment="Please deliver between 9am and 5pm"
    )
    assert order.name == "John Doe"
    assert order.email == "john.doe@example.com"
    assert order.phone == "+380509999999"
    assert order.comment == "Please deliver between 9am and 5pm"
    assert order.is_processed is True

@pytest.mark.django_db
def test_order_item_creation():
    category = ClothCategory.objects.create(name="Shirts", slug="shirts")
    cloth = Cloth.objects.create(
        name="T-Shirt",
        slug="t-shirt",
        category=category,
        genre="male",
        color="red",
        size="M",
        brand="BrandA",
        material="cotton",
        price=19.99
    )
    order = Order.objects.create(
        name="John Doe",
        email="john.doe@example.com",
        phone="+380509999999",
    )
    order_item = OrderItem.objects.create(order=order, cloth=cloth, quantity=2, total_price=39.98)
    assert order_item.order == order
    assert order_item.cloth == cloth
    assert order_item.quantity == 2
    assert order_item.total_price == 39.98

@pytest.mark.django_db
def test_invalid_phone_number():
    with pytest.raises(ValidationError):
        order = Order(
            name="John Doe",
            email="john.doe@example.com",
            phone="invalid_phone",
        )
        order.full_clean()

