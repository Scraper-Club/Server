from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from core.proxies import IPAddress
from .base import TemplateListView


@login_required
def get_all(request):
    scraper = request.user.scraper

    page = int(request.GET.get('page', '1'))

    items_list = list(scraper.get_ip_addresses())
    view = TemplateListView(items_list, 'ip/get_all.html', page=page)
    view.add_extra('ip_count', len(items_list))
    return view.render(request)


@login_required
def get(request, pk):
    scraper = request.user.scraper
    try:
        ip_address = IPAddress.objects.get(pk=pk)
    except IPAddress.DoesNotExist:
        if request.user.is_superuser:
            return redirect('admin_ips')
        else:
            return redirect('get_all_addresses')

    context = {
        'ip_address': ip_address,
        'connections_for_hour': ip_address.get_last_hour_connections().count(),
        'connections_for_day': ip_address.get_last_day_connections().count(),
        'rate_type': ip_address.get_rate_type_display(),
        'rate_limit': ip_address.rate_limit,
    }
    return render(request, 'ip/get.html', context)
