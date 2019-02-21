from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from core.proxies import Device
from core.views.base import TemplateListView


@login_required
def get_all(request):
    scraper = request.user.scraper

    page = int(request.GET.get('page', '1'))

    items_list = list(scraper.get_devices())
    devices_count = scraper.get_devices().count()
    view = TemplateListView(items_list, 'device/get_all.html', page=page)
    view.add_extra('devices_count', devices_count)
    return view.render(request)


@login_required
def delete_all(request):
    scraper = request.user.scraper
    scraper.get_devices().delete()
    return redirect('get_all_devices')


@login_required
def get(request, device_id):
    scraper = request.user.scraper
    try:
        device = scraper.get_devices().get(device_id=device_id)
    except Device.DoesNotExist:
        return redirect('get_all_devices')

    context = {
        'device': device,
    }

    return render(request, 'device/get.html', context)


@login_required
def delete(request, device_id):
    scraper = request.user.scraper
    try:
        device = scraper.get_devices().get(device_id=device_id)
    except Device.DoesNotExist:
        return redirect('get_all_devices')

    device.get_statistic().delete()
    device.current_owner = None
    device.save()

    return redirect('get_all_devices')


@login_required
def reset(request, device_id):
    scraper = request.user.scraper
    try:
        device = scraper.get_devices().get(device_id=device_id)
    except Device.DoesNotExist:
        return redirect('get_all_devices')

    stat = device.get_statistic()
    stat.scrapes_count = 0
    stat.save()

    return redirect('get_all_devices')
