import scrapy


class BusScrapyItem(scrapy.Item):
    title = scrapy.Field()
    departure = scrapy.Field()
    voyage = scrapy.Field()
    arrival = scrapy.Field()
    cost = scrapy.Field()
    status = scrapy.Field()
    place = scrapy.Field()
