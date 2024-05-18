import pytest
from django.core.exceptions import ValidationError
from main.forms import OrderForm

@pytest.mark.django_db
def test_order_form_valid_data():#Перевіряє, чи форма валідна при введенні коректних даних
    form_data = {
        'name': 'John Doe',
        'email': 'john.doe@example.com',
        'phone': '+380509999999',
        'comment': 'Please deliver between 9am and 5pm'
    }
    form = OrderForm(data=form_data)
    assert form.is_valid()

@pytest.mark.django_db
def test_order_form_invalid_email():#Перевіряє, чи форма не валідна при введенні некоректного формату електронної пошти, та чи міститься відповідна помилка
    form_data = {
        'name': 'John Doe',
        'email': 'not-an-email',
        'phone': '+380509999999',
        'comment': 'Please deliver between 9am and 5pm'
    }
    form = OrderForm(data=form_data)
    assert not form.is_valid()
    assert 'email' in form.errors

@pytest.mark.django_db
def test_order_form_invalid_phone():#Перевіряє, чи форма не валідна при введенні некоректного номера телефону, та чи міститься відповідна помилка
    form_data = {
        'name': 'John Doe',
        'email': 'john.doe@example.com',
        'phone': 'invalid_phone',
        'comment': 'Please deliver between 9am and 5pm'
    }
    form = OrderForm(data=form_data)
    assert not form.is_valid()
    assert 'phone' in form.errors

@pytest.mark.django_db
def test_order_form_missing_name():#Перевіряє, чи форма не валідна при відсутності обов'язкового поля name, та чи міститься відповідна помилка
    form_data = {
        'email': 'john.doe@example.com',
        'phone': '+380509999999',
        'comment': 'Please deliver between 9am and 5pm'
    }
    form = OrderForm(data=form_data)
    assert not form.is_valid()
    assert 'name' in form.errors
