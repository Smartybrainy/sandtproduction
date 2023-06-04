from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.db.models import Q
from snail.models import Cosmetic, Item


class CosmeticListView(ListView):
    model = Cosmetic
    queryset = Cosmetic.objects.all()
    paginate_by = 15
    template_name = 'cosmetics/cosmetic_list.html'


class CosmeticDetailView(DetailView):
    model = Cosmetic
    template_name = 'cosmetics/cosmetic_detail.html'


def cosmetic_search_item(request):
    qs = request.GET.get('qs', '')
    if qs is not None:
        item_search_result = Item.objects.filter(
            Q(title__icontains=qs) | Q(label__icontains=qs)
        )
    return render(request, 'cosmetics/cosmetic_list.html', {"object_list": item_search_result})

