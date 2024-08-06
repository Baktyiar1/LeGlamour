from django.shortcuts import render
from .models import Cosmetic
from user.forms import RegisterUserForm
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages




def index_views(request):
    cosmetics = Cosmetic.objects.filter(is_active=True)[::-1][:3]
    register_views = RegisterUserForm()

    return render(
        request=request,
        template_name='cosmo/index.html',
        context={
            'cosmetics': cosmetics,
            'form': register_views
        }
    )



def detail_views(request,pk):
    cosmetic = Cosmetic.objects.get(id=pk)
    return render(
        request=request,
        template_name='cosmo/shop-detail.html',
        context={
            'cosmetic':cosmetic,
        }
    )
