from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from main.models import Cloth
from main.models import OrderItem
from django.shortcuts import redirect
# Create your views here.
def shopItemHome(request):
    return render(request, 'shop_item.html')

def shop_item_detail(request, cloth_slug):
    cloth = get_object_or_404(Cloth, slug=cloth_slug)
    order_items = OrderItem.objects.all()
    total = sum(item.total_price for item in order_items)
    return render(request, 'shop_item.html', {'cloth': cloth, 'order_items': order_items, 'total': total})

def add_to_cart(request, cloth_id):
    cloth = get_object_or_404(Cloth, id=cloth_id)

    order_item, created = OrderItem.objects.get_or_create(
        cloth=cloth,
        defaults={'quantity': 0, 'total_price': 0}
    )

    order_item.quantity += 1
    order_item.total_price = order_item.quantity * cloth.price
    order_item.save()

    messages.success(request, f'Added {cloth.name} to your cart.')

    return render(request, 'cart_added.html')

def clear_cart(request):
    OrderItem.objects.all().delete()
    messages.success(request, 'Cart is empty.')
    return render(request, 'cart_clear.html')

def orderItem(request):
    order_items = OrderItem.objects.all()
    total = sum(item.total_price for item in order_items)
    return render(request, 'orderItem.html', {'cart_items': order_items, 'total': total})

