import io
import zipfile

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render

from core.proxies import Scrap
from core.views.base import TemplateListView


def download_as_zip(scrapes):
    zip_io = io.BytesIO()
    mapping_file = io.StringIO()

    zf = zipfile.ZipFile(zip_io, "w", zipfile.ZIP_DEFLATED, False)
    for scrap in scrapes:
        filename = str(scrap.id) + 'html'
        zf.writestr(filename + '.html', scrap.get_result_bytes())
        mapping_file.write(filename + '.html,' + str(scrap.url_value) + '\n')
    zf.writestr('mapping.csv', mapping_file.getvalue())
    zf.close()
    return HttpResponse(zip_io.getvalue(), content_type='application/x-zip-compressed')


@login_required
def get_all(request):
    scraper = request.user.scraper
    page = int(request.GET.get('page', '1'))
    items_list = list(scraper.get_scrapes())
    scrapes_count = len(items_list)
    view = TemplateListView(items_list, 'scrap/get_all.html', page=page)
    view.add_extra('scrapes_count', scrapes_count)
    return view.render(request)


@login_required
def download_all(request):
    scraper = request.user.scraper
    scrapes = scraper.get_scrapes()
    return download_as_zip(scrapes)


@login_required
def download_selected(request):
    scraper = request.user.scraper

    if request.method == 'POST':
        scrapes = scraper.get_scrapes().filter(id__in=request.POST.getlist('selected'))
        return download_as_zip(scrapes)

    return redirect('get_all_scrapes')


@login_required
def delete_all(request):
    scraper = request.user.scraper
    scraper.get_scrapes().delete()
    return redirect('get_all_scrapes')


@login_required
def get(request, scrap_id):
    scraper = request.user.scraper
    try:
        scrap = scraper.get_scrapes().get(pk=scrap_id)
    except Scrap.DoesNotExist:
        return redirect('get_all_scrapes')

    context = {
        'scrap': scrap,
    }
    return render(request, 'scrap/get.html', context)


@login_required
def get_result(request, scrap_id):
    scraper = request.user.scraper
    try:
        scrap = scraper.get_scrapes().get(pk=scrap_id)
    except Scrap.DoesNotExist:
        return redirect('get_all_scrapes')

    return HttpResponse(scrap.get_result_str('utf-8'), content_type="text/html")


@login_required
def donwload(request, scrap_id):
    scraper = request.user.scraper
    try:
        scrap = scraper.get_scrapes().get(pk=scrap_id)
    except Scrap.DoesNotExist:
        return redirect('get_all_scrapes')

    return download_as_zip([scrap])


@login_required
def delete(request, scrap_id):
    scraper = request.user.scraper
    try:
        scrap = scraper.get_scrapes().get(pk=scrap_id)
        scrap.delete()
    except Scrap.DoesNotExist:
        pass
    return redirect('get_all_scrapes')


@login_required
def complain(request, scrap_id):
    scraper = request.user.scraper
    try:
        scrap = scraper.get_scrapes().get(pk=scrap_id)
    except Scrap.DoesNotExist:
        return redirect('get_all_scrapes')

    if scrap.can_complain():
        scrap.on_complained()

    return redirect('get_scrap', scrap_id=scrap_id)
