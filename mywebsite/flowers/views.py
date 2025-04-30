from django.shortcuts import render, get_object_or_404
from .models import Flower

# Create your views here.
def index(request):
    flowers = Flower.objects.all()
    return render(request, 'flowers/index.html', {'flowers': flowers})

def detail(request, slug=None):
    flower = get_object_or_404(Flower, slug=slug)
    return render(request, 'flowers/detail.html', locals())