import scrapy
from bus_scrapy.items import BusScrapyItem
from bus_scrapy.settings import PARSER_NAME


class QuotesSpider(scrapy.Spider):
    name = PARSER_NAME
    start_urls = [
        'http://bus.com.ua/cgi-bin/tablo.pl',
    ]

    def parse(self, response):
        for row in response.xpath('//td[@nowrap]'):
            item = BusScrapyItem()
            item['title'] = row.xpath('./a/text()').get()
            try:
                yield response.follow(row.xpath('.//a/@href').get(),
                                      callback=self.parse_busstation, meta={'item': item})
            except scrapy.exceptions.NotSupported:
                continue

    def parse_busstation(self, response):
        for row in response.xpath('//tr[@bgcolor="#f2f9f9"]|tr[@bgcolor="#e2f9f9"]'):
            item = response.meta['item']
            item['departure'] = row.xpath('concat(./td[1]/font/text(), " ",./td[1]/b/text())').get()
            item['voyage'] = row.xpath('concat(./td[2]/text(), ./td[2]/a/font/b/text())').get()
            item['arrival'] = row.xpath('./td[3]/b/text()').get()
            item['cost'] = row.xpath('./td[4]/b/text()').get()
            item['status'] = row.xpath('./td[6]//text()').get()
            item['place'] = row.xpath('./td[7]/b/a/text()|./td[7]/b/text()').get()
            yield item
