from celery.task import task
from django.core.mail import send_mail
from scrapyd_api import ScrapydAPI
from bus_scrapy.settings import BOT_NAME, PARSER_NAME
from .models import Scraper


@task(name='send_mail_task')
def send_mail_task(to, subject, body):
    """
    task for sending email
    :param to:
    :param subject:
    :param body:
    :return:
    """
    send_mail(subject=subject, message=body, recipient_list=to, from_email='admin@site.com')


@task(name='check_parser_status')
def check_parser_status():
    """
    task that checks current status (running, scheduled, finished
    or empty string if scraper with selected job id not founded)
    of all scrapes on the database
    :return:
    """
    spiders = Scraper.objects.all()
    scrapyd = ScrapydAPI('http://scrapyd:6800')
    for spider in spiders:
        status = scrapyd.job_status(BOT_NAME, spider.job_id)
        spider.status = status
        spider.save(update_fields=['status'])


@task(name='scrapy_bus_station')
def scrapy_bus_station():
    """
    task that create new Scraper instance
    :return:
    """
    Scraper.objects.create()
