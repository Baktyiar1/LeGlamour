from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
from .models import Cosmetic,Category
from .forms import MyUpdateForm,CosmeticAddForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from user.forms import RegisterUserForm
from .filters import CosmeticFilters
import logging
from django.contrib.auth.decorators import user_passes_test

from django.contrib.auth import get_user_model

User = get_user_model()

def index_views(request):

    cosmetics = Cosmetic.objects.filter(is_active=True)[::-1][:3]
    register_views = RegisterUserForm()

    if request.method == 'POST':
        form = CosmeticAddForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Успешно создана')
    form = CosmeticAddForm()

    return render(
        request=request,
        template_name='cosmo/index.html',
        context={
            'cosmetics': cosmetics,
            'register_form': register_views,
            'form': form
        }
    )


# @user_passes_test(lambda u: u.is_authenticated and (u.is_admin or u.status == 2), login_url='register')
def detail_views(request,pk):

    cosmetic = get_object_or_404(Cosmetic,id=pk)

    recommendations = Cosmetic.objects.filter(category=cosmetic.category)

    if request.method == 'POST':
        if 'delete' in request.POST:
            cosmetic.delete()
            messages.success(request,'Успешно удалено')
            return redirect('index')

        form = MyUpdateForm(request.POST,request.FILES,instance=cosmetic)
        if form.is_valid():
            form.save()
            messages.success(request, 'Успешно изменено')
    form = MyUpdateForm(instance=cosmetic)

    return render(
        request=request,
        template_name='cosmo/shop-detail.html',
        context={
            'cosmetic': cosmetic,
            'recommendations': recommendations,
            'form': form,
        }
    )

logger = logging.getLogger(__name__)
def shop_view(request):
    cosmetic_filter = CosmeticFilters(request.GET,queryset=Cosmetic.objects.filter(is_active=True))
    listings = cosmetic_filter.qs
    print(listings)
    logger.debug(f'Request GET params: {request.GET}')
    logger.debug(f'Filtered queryset: {listings}')

    paginator = Paginator(listings, 6)
    page_number = request.GET.get('page')

    categories = Category.objects.all()

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
            'page_range': paginator.page_range,
            'categories': categories,
            'filter': cosmetic_filter,

        }
    )



def about_views(request):

    return render(
        request=request,
        template_name='cosmo/about.html'
    )