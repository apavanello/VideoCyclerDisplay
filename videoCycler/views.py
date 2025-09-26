from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import DisplayItem

def display_view(request):
    # Busca todos os itens, já ordenados conforme definido no modelo
    items = DisplayItem.objects.all()
    context = {'items': items}
    return render(request, 'videoCycler/index.html', context)


def check_for_updates(request):
    item_count = DisplayItem.objects.count()
    data = {
        'total_items': item_count,
    }
    return JsonResponse(data)