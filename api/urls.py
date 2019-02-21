from django.urls import path
from . import views

urlpatterns = [
    # API methods
    path('api/v1/scrapes/<int:scrap_id>/send', views.SendScrapView.as_view()),
    # path('api/v1/scrapes/send', views.SendMultiple.as_view()),

    path('api/v1/scrapes/', views.ScrapesView.as_view()),
    path('api/v1/scrapes/<int:scrap_id>',views.ScrapView.as_view()),
    path('api/v1/scrapes/<int:scrap_id>/result', views.ScrapResultView.as_view()),

    path('api/v1/urls/', views.UrlsView.as_view()),
    path('api/v1/urls/<int:url_id>/', views.UrlView.as_view()),

    path('api/v1/info/', views.ScraperUserView.as_view()),
]
