from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from apps.models import Order

@user_passes_test(lambda u: u.is_authenticated and (u.is_admin or u.status == 2), login_url='index')

def crm_views(request):

    crm_lists = Order.objects.all().order_by('-id')

    return render(
        request=request,
        template_name='crm/crm.html',
        context={
            'crm_lists': crm_lists
        }
    )
