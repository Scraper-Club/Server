from django.urls import path, include

from core import api_views
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing'),

    path('home/', views.home, name='home'),
    path('home/download/', views.download_android, name='download_android_app'),
    path('home/delete/', views.delete_user, name='delete_user'),

    # URL_model paths
    path('urls/', views.scrapurl.get_all, name='get_all_urls'),
    path('urls/delete/', views.scrapurl.delete_all, name='delete_all_urls'),
    path('urls/add/', views.scrapurl.add, name='add_urls'),
    path('urls/upload/', views.scrapurl.upload, name='upload_urls'),

    path('urls/<int:url_id>/', views.scrapurl.get, name='get_url'),
    path('urls/<int:url_id>/update/', views.scrapurl.update, name='update_url'),
    path('urls/<int:url_id>/reset/', views.scrapurl.reset, name='reset_url'),

    # Domain paths
    path('domains/', views.scrapdomain.get_all, name='get_all_domains'),
    path('domains/delete/', views.scrapdomain.delete_all, name='delete_all_domains'),
    path('api/v1/domains/', api_views.DomainsAPIView),

    path('domains/<int:domain_id>/', views.scrapdomain.get, name='get_domain'),
    path('domains/<int:domain_id>/delete/', views.scrapdomain.delete, name='delete_domain'),
    path('domains/<int:domain_id>/update/', views.scrapdomain.update, name='update_domain_config'),
    path('domains/<int:domain_id>/reset/', views.scrapdomain.reset_config, name='reset_domain_config'),
    path('domains/<int:domain_id>/blacklist/', views.scrapdomain.update_blacklist, name='update_domain_blacklist'),

    # Devices paths
    path('devices/', views.scrapdevice.get_all, name='get_all_devices'),
    path('devices/delete/', views.scrapdevice.delete_all, name='delete_all_devices'),

    path('devices/<device_id>/', views.scrapdevice.get, name='get_device'),
    path('devices/<device_id>/delete/', views.scrapdevice.delete, name='delete_device'),
    path('devices/<device_id>/reset/', views.scrapdevice.reset, name='reset_device'),

    # Scrap paths
    path('scrapes/', views.scrapresult.get_all, name='get_all_scrapes'),
    path('scrapes/download/', views.scrapresult.download_all, name='download_all_scrapes'),
    path('scrapes/selected/download/', views.scrapresult.download_selected, name='download_selected_scrapes'),
    path('scrapes/delete/', views.scrapresult.delete_all, name='delete_all_scrapes'),

    path('scrapes/<int:scrap_id>/', views.scrapresult.get, name='get_scrap'),
    path('scrapes/<int:scrap_id>/result', views.scrapresult.get_result, name='get_scrap_result'),
    path('scrapes/<int:scrap_id>/download', views.scrapresult.donwload, name='download_scrap'),
    path('scrapes/<int:scrap_id>/delete', views.scrapresult.delete, name='delete_scrap'),
    path('scrapes/<int:scrap_id>/complain', views.scrapresult.complain, name='complain_scrap'),

    # IP paths
    path('addresses/', views.ip_address.get_all, name='get_all_addresses'),
    path('addresses/<pk>', views.ip_address.get, name='get_address_info'),

    path('signup/', views.auth.SignupView.as_view(), name='signup'),

    path('api/v1/ip/<pk>/',api_views.IPAddressAPIView.as_view(), name='api_manage_ip'),
]
