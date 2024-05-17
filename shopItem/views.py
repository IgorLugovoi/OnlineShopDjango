from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from main.models import Cloth, Order
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

# def add_to_cart(request, cloth_id):
#     cloth = get_object_or_404(Cloth, id=cloth_id)
#     order_item, created = OrderItem.objects.get_or_create(
#         cloth=cloth,
#         defaults={'quantity': 0, 'total_price': 0}
#     )
#
#     order_item.quantity += 1
#     order_item.total_price = order_item.quantity * cloth.price
#     order_item.save()
#
#     messages.success(request, f'Added {cloth.name} to your cart.')
#
#     return render(request, 'cart_added.html')
def add_to_cart(request, cloth_id):
    cloth = get_object_or_404(Cloth, id=cloth_id)

    cart = request.session.get('cart', {})

    if str(cloth_id) not in cart:
        cart[str(cloth_id)] = {'quantity': 1, 'total_price': str(cloth.price)}
    else:
        cart[str(cloth_id)]['quantity'] += 1
        cart[str(cloth_id)]['total_price'] = str(cloth.price * cart[str(cloth_id)]['quantity'])

    request.session['cart'] = cart
    messages.success(request, f'Added {cloth.name} to your cart.')

    return render(request, 'cart_added.html')

def clear_cart(request):
    request.session['cart'] = {}
    # OrderItem.objects.all().delete()
    messages.success(request, 'Cart is empty.')
    return render(request, 'cart_clear.html')

# def orderItem(request):
#     order_items = OrderItem.objects.all()
#     total = sum(item.total_price for item in order_items)
#     return render(request, 'orderItem.html', {'cart_items': order_items, 'total': total})
def orderItem(request):
    cart = request.session.get('cart', {})
    order_items = []

    for cloth_id, item in cart.items():
        cloth = get_object_or_404(Cloth, id=int(cloth_id))
        order_item = {
            'cloth': cloth,
            'quantity': item['quantity'],
            'total_price': item['total_price']
        }
        order_items.append(order_item)

    total = sum(float(item['total_price']) for item in order_items)
    return render(request, 'orderItem.html', {'order_items': order_items, 'total': total})


