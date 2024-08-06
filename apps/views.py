from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from .models import Cosmetic


def index_views(request):
    cosmetics = Cosmetic.objects.filter(is_active=True)[::-1][:3]

    return render(
        request=request,
        template_name='cosmo/index.html',
        context={
            'cosmetics': cosmetics,
        }
    )


def detail_views(request, pk):
    cosmetic = Cosmetic.objects.get(id=pk)

    return render(
        request=request,
        template_name='cosmo/shop-detail.html',
        context={
            'cosmetic': cosmetic,
        }
    )


def shop_view(request):
    cosmetics = Cosmetic.objects.filter(is_active=True).order_by('-id')  # Сортировка по убыванию ID
    paginator = Paginator(cosmetics, 6)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(
        request=request,
        template_name='cosmo/shop.html',
        context={
            'cosmetics': page_obj,
            'page_obj': page_obj,
            'page_range': paginator.page_range
        }
    )
