from django.shortcuts import render
from .models import ClothCategory
from .forms import OrderForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Cloth
from .models import CartItem
from django.db.models import Sum
# Create your views here.
def home(request):
    categories = ClothCategory.objects.filter(is_visible=True)
    form = OrderForm()
    cart_items = CartItem.objects.all()
    total_price = CartItem.objects.aggregate(total=Sum('cloth__price'))['total'] or 0

    return render(request, 'main.html ', context= {
        'categories': categories,
        'form': form,
        'cart_items': cart_items,
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
#     return render(request, 'cartItem.html', {'cart_items': cart_items})

def view_cart_and_order(request):
    cart_items = CartItem.objects.all()  # Отримуємо всі елементи кошика

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your order has been successfully submitted!')
            return redirect('home')
        else:
            messages.error(request, 'Something went wrong!')
    else:
        form = OrderForm()

    context = {
        'cart_items': cart_items,
        'form': form,
    }

    return render(request, 'cartItem.html', context)
