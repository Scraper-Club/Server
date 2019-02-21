from django.urls import path
from . import views

urlpatterns = [

    path('api/scrap/<int:url_id>/upload/', views.UploadUrlView.as_view()),
    path('api/auth/login/', views.Login.as_view()),
    path('api/auth/check/', views.CheckApiKey.as_view()),

    path('api/device/register/', views.Register.as_view()),
    path('api/device/check/', views.Check.as_view()),
    path('api/device/stats/', views.Stats.as_view()),

    path('api/v1/geturl/', views.GetNextURL.as_view()),

    path('api/v1/url/<int:url_id>/bad/', views.BadUrlView.as_view()),

]
