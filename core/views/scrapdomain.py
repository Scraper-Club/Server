from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from core.forms import ConfigurationForm
from core.models import UrlStatus
from core.proxies import Domain, IPAddress, Device, IPConnection
from .base import TemplateListView


@login_required
def get_all(request):
    scraper = request.user.scraper
    page = int(request.GET.get('page', '1'))
    items_list = list(scraper.get_domains())
    domains_count = scraper.get_domains().count()
    view = TemplateListView(items_list, 'domain/get_all.html', page=page)
    view.add_extra('domains_count', domains_count)
    return view.render(request)


@login_required
def delete_all(request):
    scraper = request.user.scraper
    scraper.get_domains().delete()
    return redirect('get_all_urls')


@login_required
def get(request, domain_id):
    scraper = request.user.scraper
    try:
        domain = scraper.get_domains().get(pk=domain_id)
    except Domain.DoesNotExist:
        return redirect('get_all_domains')

    ip_addresses = IPAddress.objects.all()
    devices = Device.objects.all()
    context = {
        'domain': domain,
        'form_configs': ConfigurationForm(instance=domain.configuration),
        'urls_count': scraper.get_urls().filter(domain=domain).count(),
        'scraped_urls': scraper.get_urls().filter(domain=domain, status=UrlStatus.SCRAPED).count(),
        'connections_for_hour': IPConnection.hourly.filter(domain=domain).count(),
        'connections_for_day': IPConnection.daily.filter(domain=domain).count(),
        'ip_address_choice': ip_addresses.difference(domain.blacklist.ip_addresses.all()),
        'blocked_ip_addresses': domain.blacklist.ip_addresses.all(),
        'device_choices': devices.difference(domain.blacklist.devices.all()),
        'blocked_devices': domain.blacklist.devices.all(),
    }
    return render(request, 'domain/get.html', context)


@login_required
def update(request, domain_id):
    scraper = request.user.scraper
    try:
        domain = scraper.get_domains().get(pk=domain_id)
    except Domain.DoesNotExist:
        return redirect('get_all_domains')

    if request.method == 'POST':
        f = ConfigurationForm(request.POST, instance=domain.configuration)
        configs = f.save()
        configs.save()

    return redirect('get_domain', domain_id=domain_id)


@login_required
def delete(request, domain_id):
    scraper = request.user.scraper
    try:
        domain = scraper.get_domains().get(pk=domain_id)
        domain.delete()
    except Domain.DoesNotExist:
        pass

    return redirect('get_all_domains')


@login_required
def reset_config(request, domain_id):
    scraper = request.user.scraper
    try:
        domain = scraper.get_domains().get(pk=domain_id)
    except Domain.DoesNotExist:
        return redirect('get_all_domains')

    domain.reset_config()

    return redirect('get_domain', domain_id=domain_id)


@login_required
def update_blacklist(request, domain_id):
    scraper = request.user.scraper
    try:
        domain = scraper.get_domains().get(pk=domain_id)
    except Domain.DoesNotExist:
        return redirect('get_all_domains')

    if request.method == 'POST':
        print(request.POST)
        choosed_ips = request.POST.getlist('choosed_ip')
        choosed_devices = request.POST.getlist('choosed_devices')

        domain.blacklist.devices.clear()
        domain.blacklist.ip_addresses.clear()

        if len(choosed_ips) !=0:
            choosed_ips = IPAddress.objects.filter(ip_address__in=choosed_ips)
            domain.blacklist.ip_addresses.add(*choosed_ips)

        if len(choosed_devices) != 0:
            choosed_devices = Device.objects.filter(device_id__in=choosed_devices)
            domain.blacklist.devices.add(*choosed_devices)

    return redirect('get_domain', domain_id=domain_id)
