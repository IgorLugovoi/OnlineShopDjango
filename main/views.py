from django.shortcuts import render
from .models import ClothCategory

# Create your views here.
def home(request):
    categories = ClothCategory.objects.filter(is_visible=True)

    return render(request, 'main.html ', context= {
        'categories': categories,
    })