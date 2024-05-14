from django.shortcuts import render
from main.models import Cloth

# Create your views here.
# def ItemListHome(request):
#     return render(request, 'itemList.html')

def ItemListHome(request):
    clothes = Cloth.objects.all()
    return render(request, 'ItemList.html', {'clothes': clothes})
