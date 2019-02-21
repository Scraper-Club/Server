from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render


@login_required
def home(request):
    context = {
        'scraper': request.user.scraper,
        'android': 'android' in request.META['HTTP_USER_AGENT'].lower(),
    }

    return render(request, 'home.html', context)


def download_android(request):
    with open('files/scraper.apk', 'rb') as apk:
        response = HttpResponse(apk.read(), content_type="application/vnd.android.package-archive")
        response['Content-Disposition'] = 'inline; filename=scraper.apk'

    return response


@login_required
def delete_user(request):
    request.user.delete()
    logout(request)
    return redirect('login')


def landing_page(request):
    return render(request, 'landing.html')
