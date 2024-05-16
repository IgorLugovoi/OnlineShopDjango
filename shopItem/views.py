from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from main.models import Cloth
from main.models import CartItem
from django.shortcuts import redirect
# Create your views here.
def shopItemHome(request):
    return render(request, 'shop_item.html')

def shop_item_detail(request, cloth_slug):
    cloth = get_object_or_404(Cloth, slug=cloth_slug)
    cart_items = CartItem.objects.all()
    total = sum(item.total_price for item in cart_items)
    return render(request, 'shop_item.html', {'cloth': cloth, 'cart_items': cart_items, 'total': total})

def add_to_cart(request, cloth_id):
    cloth = get_object_or_404(Cloth, id=cloth_id)

    cart_item, created = CartItem.objects.get_or_create(
        cloth=cloth,
        defaults={'quantity': 0, 'total_price': 0}
    )

    cart_item.quantity += 1
    cart_item.total_price = cart_item.quantity * cloth.price
    cart_item.save()

    messages.success(request, f'Added {cloth.name} to your cart.')

    return render(request, 'cart_added.html')

def clear_cart(request):
    CartItem.objects.all().delete()
    messages.success(request, 'Cart is empty.')
    return render(request, 'cart_clear.html')

def cartItem(request):
    cart_items = CartItem.objects.all()
    total = sum(item.total_price for item in cart_items)
    return render(request, 'cartItem.html', {'cart_items': cart_items, 'total': total})

