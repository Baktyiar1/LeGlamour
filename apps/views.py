from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
from .models import Cosmetic,Category
from .forms import MyUpdateForm,CosmeticAddForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from user.forms import RegisterUserForm
from django.contrib.auth.decorators import user_passes_test


@user_passes_test(lambda u: u.is_authenticated and (u.is_admin or u.status == 2), login_url='index')
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


def shop_view(request):
    cosmetics = Cosmetic.objects.filter(is_active=True).order_by('-id')  # Сортировка по убыванию ID
    paginator = Paginator(cosmetics, 6)
    page_number = request.GET.get('page')

    categories = Category.objects.all()

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    if request.method == 'POST':
        form = CosmeticAddForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Успешно создана')
    form = CosmeticAddForm()

    return render(
        request=request,
        template_name='cosmo/shop.html',
        context={
            'cosmetics': page_obj,
            'page_obj': page_obj,
            'page_range': paginator.page_range,
            'form': form,
            'categories': categories

        }
    )



def about_views(request):

    return render(
        request=request,
        template_name='cosmo/about.html'
    )