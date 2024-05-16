from django.shortcuts import render
from .models import ClothCategory
from .forms import OrderForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Cloth
from .models import OrderItem
from django.db.models import Sum
# Create your views here.
def home(request):
    categories = ClothCategory.objects.filter(is_visible=True)
    form = OrderForm()
    order_items = OrderItem.objects.all()
    total_price = OrderItem.objects.aggregate(total=Sum('cloth__price'))['total'] or 0

    return render(request, 'main.html ', context= {
        'categories': categories,
        'form': form,
        'order_items': order_items,
        'total_price': total_price,
    })

# def order_view(request):
#     if request.method == 'POST':
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Your order has been successfully submitted!')
#         else:
#             messages.error(request, 'Something went wrong!')
#         return redirect('home')
#     else:
#         form = OrderForm()
#     return render(request, 'order.html', {'form': form})

# views.py
def show_category_items(request, category_id):
    category = ClothCategory.objects.get(id=category_id)
    items = Cloth.objects.filter(category=category_id)
    return render(request, 'category_items.html', {'category': category, 'items': items})

# def view_cart(request):
#     cart_items = CartItem.objects.all() # Отримуємо всі елементи кошика
#     return render(request, 'orderItem.html', {'cart_items': cart_items})

def view_cart_and_order(request):
    order_items = OrderItem.objects.all()  # Отримуємо всі елементи кошика

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in order_items:
                OrderItem.objects.create(
                    order=order,
                    cloth=item.cloth,
                    quantity=item.quantity,
                    total_price=item.total_price
                )
            messages.success(request, 'Your order has been successfully submitted!')
            return redirect('home')
        else:
            messages.error(request, 'Something went wrong!')
    else:
        form = OrderForm()

    context = {
        'order_items': order_items,
        'form': form,
    }

    return render(request, 'orderItem.html', context)
