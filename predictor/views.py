from django.shortcuts import render
from .models import Laptop
# Create your views here.
def index(request):
    laptops = Laptop.objects.all()
    return render(request, 'predictor/index.html', {'laptops': laptops})