# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BusScrapyItem(scrapy.Item):
    title = scrapy.Field()
    departure = scrapy.Field()
    voyage = scrapy.Field()
    arrival = scrapy.Field()
    cost = scrapy.Field()
    status = scrapy.Field()
    place = scrapy.Field()
