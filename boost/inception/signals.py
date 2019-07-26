import os
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from scrapyd_api import ScrapydAPI
from bus_scrapy.settings import BOT_NAME, PARSER_NAME
from .models import Scraper, Images


@receiver(post_save, sender=Scraper)
def run_spider(sender, instance, created, **kwargs):
    if created:
        scrapyd = ScrapydAPI('http://scrapyd:6800')
        job_id = scrapyd.schedule(BOT_NAME, PARSER_NAME)
        if job_id:
            instance.job_id = job_id
            instance.save(update_fields=['job_id'])


@receiver(post_delete, sender=Images)
def delete_image(sender, instance, **kwargs):
    os.remove(instance.image.path)
