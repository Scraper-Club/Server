from django.urls import path
from . import views

urlpatterns = [
    path('admin/home/', views.home, name='admin_home'),
    path('admin/devices/', views.devices, name='admin_devices'),
    path('admin/users/', views.users, name='admin_users'),
    path('admin/ips/', views.addresses, name='admin_ips'),
    path('admin/urls/', views.scrapurls, name='admin_urls'),
    path('admin/complains/', views.complains, name='admin_complains'),

    path('admin/urls/<pk>/delete/', views.delete_url, name='admin_url_delete'),
    path('admin/device/<device_id>/block/', views.block_device, name='block_device'),
    path('admin/device/<device_id>/unblock/', views.unblock_device, name='unblock_device'),
    path('admin/user/<int:user_id>/tokens/', views.set_tokens, name='set_tokens'),
    path('admin/user/<int:user_id>/mode/', views.change_mode, name='change_mode'),

    path('admin/tokens_rate/', views.set_token_rate_rules, name='tokens_rate'),
]