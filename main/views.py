from django.shortcuts import render, get_object_or_404
from .models import ClothCategory
from .forms import OrderForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Cloth
from .models import OrderItem
from django.db.models import Sum
# def home(request):
#     categories = ClothCategory.objects.filter(is_visible=True)
#     form = OrderForm()
#     order_items = OrderItem.objects.all()
#     total_price = OrderItem.objects.aggregate(total=Sum('cloth__price'))['total'] or 0
#
#     return render(request, 'main.html ', context={
#         'categories': categories,
#         'form': form,
#         'order_items': order_items,
#         'total_price': total_price,
#     })
def home(request):
    categories = ClothCategory.objects.filter(is_visible=True)
    form = OrderForm()

    # Отримання товарів з сесії
    # cart = request.session.get('cart', {})
    # order_items = []
    #
    # for cloth_id, item in cart.items():
    #     cloth = get_object_or_404(Cloth, id=int(cloth_id))
    #     order_item = {
    #         'cloth': cloth,
    #         'quantity': item['quantity'],
    #         'total_price': float(item['total_price'])
    #     }
    #     order_items.append(order_item)
    #
    # total_price = sum(item['total_price'] for item in order_items)
    order_items,total_price = get_order_items(request)
    return render(request, 'main.html', context={
        'categories': categories,
        'form': form,
        'order_items': order_items,
        'total_price': total_price,
    })

def show_category_items(request, category_id):
    category = ClothCategory.objects.get(id=category_id)
    items = Cloth.objects.filter(category=category_id)
    return render(request, 'category_items.html', {'category': category, 'items': items})

# def view_cart_and_order(request):
#     order_items = OrderItem.objects.all()  # Отримуємо всі елементи кошика
#
#     if request.method == 'POST':
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             order = form.save()
#             for item in order_items:
#                 OrderItem.objects.create(
#                     order=order,
#                     cloth=item.cloth,
#                     quantity=item.quantity,
#                     total_price=item.total_price
#                 )
#             messages.success(request, 'Your order has been successfully submitted!')
#             # OrderItem.objects.all().delete() нужно удалять из корзины, а не из бд
#             return redirect('home')
#         else:
#             messages.error(request, 'Something went wrong!')
#     else:
#         form = OrderForm()
#
#     context = {
#         'order_items': order_items,
#         'form': form,
#     }
#
#     return render(request, 'orderItem.html', context)

def view_cart_and_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.is_processed = False
            order.save()

            cart = request.session.get('cart', {})
            for cloth_id, item in cart.items():
                cloth = get_object_or_404(Cloth, id=int(cloth_id))
                OrderItem.objects.create(
                    order=order,
                    cloth=cloth,
                    quantity=item['quantity'],
                    total_price=item['total_price']
                )

            # Очистимо кошик після створення замовлення
            request.session['cart'] = {}

            messages.success(request, 'Order created successfully.')
            return redirect('home')
    else:
        form = OrderForm()

    # Отримання даних з сесії
    # cart = request.session.get('cart', {}) ##данные дублируются
    # order_items = []
    #
    # for cloth_id, item in cart.items():
    #     cloth = get_object_or_404(Cloth, id=int(cloth_id))
    #     order_item = {
    #         'cloth': cloth,
    #         'quantity': item['quantity'],
    #         'total_price': float(item['total_price'])
    #     }
    #     order_items.append(order_item)
    #
    # total_price = sum(item['total_price'] for item in order_items)
    order_items,total_price = get_order_items(request)

    return render(request, 'orderItem.html', context={
        'form': form,
        'order_items': order_items,
        # 'total_price': total_price,
    })

def get_order_items(request):
    cart = request.session.get('cart', {})  ##данные дублируются
    order_items = []

    for cloth_id, item in cart.items():
        cloth = get_object_or_404(Cloth, id=int(cloth_id))
        order_item = {
            'cloth': cloth,
            'quantity': item['quantity'],
            'total_price': float(item['total_price'])
        }
        order_items.append(order_item)

    total_price = sum(item['total_price'] for item in order_items)
    return order_items,total_price
