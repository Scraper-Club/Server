import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from core.models import Scraper, ScrapComplainModel, TokenRuleModel
from core.proxies import Url, Device, IPAddress, Complain, TokenRuleChain
from core.views.base import TemplateListView


@login_required
def home(request):
    if not request.user.is_superuser:
        return redirect('home')

    total_users = Scraper.objects.all().count()
    total_devices = Device.objects.all().count()
    total_urls = Url.objects.all().count()
    public_urls = Url.public_pool.all().count()
    total_ip = IPAddress.objects.all().count()
    total_complains = ScrapComplainModel.objects.all().count()

    context = {
        'total_users': total_users,
        'total_devices': total_devices,
        'total_urls': total_urls,
        'total_ip': total_ip,
        'total_complains': total_complains,
        'public_urls': public_urls,
    }

    return render(request, 'admin/home.html', context)


@login_required
def users(request):
    if not request.user.is_superuser:
        return redirect('home')

    page = int(request.GET.get('page', '1'))
    items_list = list(Scraper.objects.all().order_by('-id'))
    items_count = len(items_list)

    view = TemplateListView(items_list, 'admin/users.html', page=page)
    view.add_extra('items_count', items_count)
    return view.render(request)


@login_required
def devices(request):
    if not request.user.is_superuser:
        return redirect('home')

    page = int(request.GET.get('page', '1'))
    items_list = list(Device.objects.all())
    items_count = len(items_list)

    view = TemplateListView(items_list, 'admin/devices.html', page=page)
    view.add_extra('items_count', items_count)
    return view.render(request)


@login_required
def addresses(request):
    if not request.user.is_superuser:
        return redirect('home')

    page = int(request.GET.get('page', '1'))
    items_list = list(IPAddress.objects.all())
    items_count = len(items_list)

    view = TemplateListView(items_list, 'admin/addresses.html', page=page)
    view.add_extra('items_count', items_count)
    return view.render(request)


@login_required
def scrapurls(request):
    if not request.user.is_superuser:
        return redirect('home')

    page = int(request.GET.get('page', '1'))
    pool = request.GET.get('pool', 'all')
    status = request.GET.get('status', 'all')

    if pool == 'all':
        query_set = Url.objects.all()
    elif pool == 'private':
        query_set = Url.private_pool.all()
    elif pool == 'public':
        query_set = Url.public_pool.all()

    if status == 'all':
        pass
    elif status == 'scraping':
        query_set = query_set.scraping()
    elif status == 'not_scraped':
        query_set = query_set.available_for_scraping()
    elif status == 'scraped':
        query_set = query_set.scraped()

    items_list = list(query_set)
    items_count = len(items_list)

    view = TemplateListView(items_list, 'admin/scrapurls.html', page=page)
    view.add_extra('items_count', items_count)
    return view.render(request)


@login_required
def complains(request):
    if not request.user.is_superuser:
        return redirect('home')

    page = int(request.GET.get('page', '1'))
    items_list = list(Complain.objects.all())
    items_count = len(items_list)

    view = TemplateListView(items_list, 'admin/complains.html', page=page)
    view.add_extra('items_count', items_count)
    return view.render(request)


@login_required
def block_device(request, device_id):
    if not request.user.is_superuser:
        return redirect('home')
    try:
        device = Device.objects.get(pk=device_id)
        device.block()
    except Device.DoesNotExist:
        pass
    finally:
        return redirect('admin_devices')


@login_required
def unblock_device(request, device_id):
    if not request.user.is_superuser:
        return redirect('home')

    try:
        device = Device.objects.get(pk=device_id)
        device.unblock()
    except Device.DoesNotExist:
        pass
    finally:
        return redirect('admin_devices')


@login_required
def set_tokens(request, user_id):
    if not request.user.is_superuser:
        return redirect('home')
    try:
        user = Scraper.objects.get(id=user_id)
    except Scraper.DoesNotExist:
        return redirect('admin_users')

    if request.method == 'GET':
        context = {
            'user': user,
        }
        return render(request, 'admin/set_token.html', context)
    elif request.method == 'POST':
        token_amount = int(request.POST.get('token_amount', '0'))
        if token_amount >= 0:
            user.set_tokens(token_amount)
        return redirect('admin_users')


@login_required
def set_token_rate_rules(request):
    if not request.user.is_superuser:
        return redirect('home')

    rules_chain, created = TokenRuleChain.objects.get_or_create(id=1)
    if created:
        rules_chain.save()

    if request.method == 'GET':
        context = {
            'current_rules': str(rules_chain).replace('[', '[\n').replace(']', '\n]').replace('}, ', '},\n'),
        }
        return render(request, 'admin/token_rate_rules.html', context)

    elif request.method == 'POST':
        rules = request.POST.get('rules', '')
        if rules:
            rules_json = json.loads(rules)
            tmp_rules_chain = TokenRuleChain(id=2)
            tmp_rules_chain.save()
            for rule_json in rules_json:
                if rule_json['to'] == 'infinite':
                    rule_json['to'] = -1
                rule = TokenRuleModel(
                    from_scrapes_count=rule_json['from'],
                    to_scrapes_count=rule_json['to'],
                    scrapes_per_token=rule_json['rate'])
                rule.save()
                tmp_rules_chain.add_rule(rule)

            if tmp_rules_chain.validate_chain():
                rules_chain.token_rules.all().delete()
                for rule in tmp_rules_chain.token_rules.all():
                    rules_chain.token_rules.add(rule)

            tmp_rules_chain.delete()

        return redirect('admin_home')


@login_required
def change_mode(request, user_id):
    if not request.user.is_superuser:
        return redirect('home')
    try:
        user = Scraper.objects.get(pk=user_id)
        mode = request.GET.get('mode', 'public')
        if mode == 'public':
            user.allow_private = False
        elif mode == 'private':
            user.allow_private = True
        user.save()
    except Scraper.DoesNotExist:
        pass

    return redirect('admin_users')

@login_required
def delete_url(request, pk):
    if not request.user.is_superuser:
        return redirect('home')
    try:
        url = Url.objects.get(pk=pk)
        url.delete()
    except Scraper.DoesNotExist:
        pass

    return redirect('admin_urls')
