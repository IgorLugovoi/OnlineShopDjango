from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from main.models import Cloth

# Create your views here.
def shopItemHome(request):
    return render(request, 'shop_item.html')



def shop_item_detail(request, cloth_slug):
    cloth = get_object_or_404(Cloth, slug=cloth_slug)
    return render(request, 'shop_item.html', {'cloth': cloth})
