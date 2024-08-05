from django.shortcuts import render
from .models import Cosmetic
def index_views(request):
    cosmetics = Cosmetic.objects.filter(is_active=True)[::-1][:3]

    return render(
        request=request,
        template_name='cosmo/index.html',
        context={
            'cosmetics':cosmetics,
        }
    )
