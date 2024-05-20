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
    order_items, total_price = get_order_items(request)
    return render(request, 'main.html', context={
        'categories': categories,
        'form': form,
        'order_items': order_items,
        'total_price': total_price,
    })


def show_category_items(request, category_id):
    category = ClothCategory.objects.get(id=category_id)
    items = Cloth.objects.filter(category=category_id)

    sizes = Cloth.SIZE_CHOICES
    colors = Cloth.COLOR_CHOICES
    materials = Cloth.MATERIAL_CHOICES

    selected_size = request.GET.get('size')
    selected_price = request.GET.get('price')
    selected_color = request.GET.get('color')
    selected_material = request.GET.get('material')

    # Apply sorting and filtering based on user selections
    items = sort_items(items, size=selected_size, price=selected_price,
                       color=selected_color, material=selected_material)

    return render(request, 'category_items.html', {
        'category': category,
        'items': items,
        'sizes': [size[0] for size in sizes],
        'colors': [color[0] for color in colors],
        'materials': [material[0] for material in materials],
        'selected_size': selected_size,
        'selected_price': selected_price,
        'selected_color': selected_color,
        'selected_material': selected_material,
    })
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

            request.session['cart'] = {}
            messages.success(request, 'Order created successfully.')
            return redirect('home')
    else:
        form = OrderForm()

    order_items, total_price = get_order_items(request)

    return render(request, 'orderItem.html', context={
        'form': form,
        'order_items': order_items,
    })


def sort_items(items, size=None, price=None, color=None, material=None):
    size_order = ['XS', 'S', 'M', 'L', 'XL', 'XXL']

    if size:
        items = items.filter(size=size)

    if color:
        items = items.filter(color=color)

    if material:
        items = items.filter(material=material)

    if price == 'asc':
        items = items.order_by('price')
    elif price == 'desc':
        items = items.order_by('-price')
    else:
        # Sort by size order if no price sorting is specified
        items = sorted(items, key=lambda x: size_order.index(x.size))

    return items


def get_order_items(request):
    cart = request.session.get('cart', {})
    order_items = []

    for cloth_id, item in cart.items():
        cloth = get_object_or_404(Cloth, id=int(cloth_id))
        order_item = {
            'cloth': cloth,
            'quantity': item['quantity'],
            'total_price': float(item['total_price'])
        }
        order_items.append(order_item)

    # Sort the order items by size
    order_items.sort(key=lambda x: x['cloth'].get_size_index())

    total_price = sum(item['total_price'] for item in order_items)
    return order_items, total_price
