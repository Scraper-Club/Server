from celery.schedules import crontab
from datetime import datetime, timedelta

from core.proxies import Url, Scrap

from scraper.celery import app


@app.task
def refresh_scraping(minutes=5):
    """
    Updates 'SCRAPING' more then 5 minutes URLs into 'NOT_SCRAPED'
    """
    Url.objects.refresh_scraping(minutes)


# TODO delete urls with scraps
@app.task
def remove_old_scrapes(days=10):
    """
    Removes old scrapes (more then 10 days) and scrapped URLs
    """
    time_threshold = datetime.now() - timedelta(days=days)
    Scrap.objects.filter(upload_date__lt=time_threshold).delete()


app.conf.beat_schedule = {
    # Every minute
    'refresh urls': {
        'task': 'core.tasks.refresh_scraping',
        'schedule': 60.0,
    },
    # Every day in 12:00
    'remove_old_scrapes': {
        'task': 'core.tasks.remove_old_scrapes',
        'schedule': crontab(hour=12, minute=0),
    },
}
