from urllib.parse import urlsplit

from django.utils.datastructures import MultiValueDictKeyError

from core.forms import ConfigurationForm
from .base import TemplateListView

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from core.models import UrlPool, UrlStatus, ConfigurationModel
from core.proxies import Domain, Url

import re

@login_required
def get_all(request):
    scraper = request.user.scraper

    page = int(request.GET.get('page', '1'))
    pool = request.GET.get('pool', 'all')
    status = request.GET.get('status', 'all')

    if pool == 'all':
        query_set = scraper.get_urls().order_by('-id')
    elif pool == 'private':
        query_set = scraper.get_private_urls().order_by('-id')
    elif pool == 'public':
        query_set = scraper.get_public_urls().order_by('-id')
    elif pool == 'waiting':
        query_set = scraper.get_waiting_urls().order_by('-id')

    if status == 'all':
        pass
    elif status == 'scraping':
        query_set = query_set.scraping()
    elif status == 'not_scraped':
        query_set = query_set.available_for_scraping()
    elif status == 'scraped':
        query_set = query_set.scraped()

    items_list = list(query_set.order_by('-id'))
    domains_count = scraper.get_domains().count()
    view = TemplateListView(items_list, 'url/get_all.html', page=page)
    view.add_extra('domains_count', domains_count)
    return view.render(request)


@login_required
def delete_all(request):
    scraper = request.user.scraper
    pool = request.GET.get('pool', '')
    if not pool:
        scraper.delete_urls()
    elif pool == 'private':
        scraper.delete_private_pool()
    elif pool == 'public':
        scraper.delete_public_pool()
    elif pool == 'waiting':
        scraper.get_waiting_urls().delete()

    return redirect('get_all_urls')


@login_required
def upload(request):
    if request.method == 'GET':
        req_pool = request.GET.get('pool', 'waiting')
        return render(request, 'url/upload.html', {'pool': req_pool})

    elif request.method == 'POST':
        try:
            uploaded = request.FILES['urls_file']
        except MultiValueDictKeyError:
            return redirect('get_all_urls')

        f = uploaded.open(mode='rb')
        urls_list = []

        regex = re.compile(
            r'^(?:http)s?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        for line in f.read().splitlines():
            if re.match(regex, line.decode('utf-8')) is not None:
                urls_list.append(line.decode('utf-8'))
        f.close()

        for url_value in urls_list:
            domain, created = Domain.objects.get_or_create(
                hostname="{0.netloc}".format(urlsplit(url_value)),
                owner=request.user
            )
            Url.objects.create(owner=request.user, url=url_value, domain=domain)

        return redirect('get_all_urls')


@login_required
def add(request):
    if request.method == 'GET':
        pool = request.GET.get('pool', 'waiting')
        return render(request, 'url/add.html', {'pool': pool, 'tokens': request.user.scraper.tokens})

    elif request.method == 'POST':
        count = int(request.POST['count'])

        for url_index in range(1, count + 1):
            key = 'url_' + str(url_index)
            url_value = request.POST[key]
            domain, created = Domain.objects.get_or_create(
                hostname="{0.netloc}".format(urlsplit(url_value)),
                owner=request.user
            )
            Url.objects.create(owner=request.user, url=url_value, domain=domain)

        return redirect('get_all_urls')


@login_required
def get(request, url_id):
    scraper = request.user.scraper
    try:
        url = scraper.get_urls().get(pk=url_id)
    except Url.DoesNotExist:
        return redirect('get_all_urls')

    context = {
        'url': url,
        'banned_ips': url.domain.blacklist.ip_addresses.all(),
        'form_configs': ConfigurationForm(instance=url.get_configuration())
    }
    return render(request, 'url/get.html', context)


@login_required
def update(request, url_id):
    print(request.POST)
    scraper = request.user.scraper
    try:
        url = scraper.get_urls().get(pk=url_id)
    except Url.DoesNotExist:
        return redirect('get_all_urls')

    if request.method == 'POST':
        if url.configuration:
            f = ConfigurationForm(request.POST, instance=url.configuration)
        else:
            f = ConfigurationForm(request.POST, instance=ConfigurationModel.objects.create(user=request.user))
        configs = f.save()
        configs.save()
        url.configuration = configs
        url.save()

    return redirect('get_url', url_id=url_id)


@login_required
def reset(request, url_id):
    scraper = request.user.scraper
    try:
        url = scraper.get_urls().get(pk=url_id)
    except Url.DoesNotExist:
        return redirect('get_all_urls')

    if url.configuration:
        url.configuration.delete()
    return redirect('manage_url', url_id=url_id)
