from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
from .models import Cosmetic,Category
from .forms import MyUpdateForm,CosmeticAddForm
def index_views(request):
    cosmetics = Cosmetic.objects.filter(is_active=True)[::-1][:3]

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
            'cosmetics':cosmetics,
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
