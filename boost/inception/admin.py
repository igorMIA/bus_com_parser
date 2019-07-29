from django.contrib import admin
from scrapyd_api import ScrapydAPI
from .models import BusStation, Images, Scraper
from bus_scrapy.settings import BOT_NAME, PARSER_NAME


class ScraperAdmin(admin.ModelAdmin):
    actions = ['stop_scraper']
    list_display = ['job_id', 'status', 'created']

    def stop_scraper(self, request, queryset):
        """
        action for stoping selected scraper
        :param request:
        :param queryset:
        :return:
        """
        for spider in queryset:
            if spider.job_id:
                scrapyd = ScrapydAPI('http://scrapyd:6800')
                scrapyd.cancel(BOT_NAME, spider.job_id, signal='TERM')
                spider.status = 'finished'
                spider.save(update_fields=['status'])
                self.message_user(request, f'id:{spider.job_id} stopped')
            else:
                self.message_user(request, 'Error')
    stop_scraper.short_description = 'Stop scraper'


admin.site.register(BusStation)
admin.site.register(Images)
admin.site.register(Scraper, ScraperAdmin)
