# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Demo1Item(scrapy.Item):
    text = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()

class BiddingItem(scrapy.Item):
    collection = 'test'
    id = scrapy.Field()
    title = scrapy.Field()
    publish_time = scrapy.Field()
    elements = scrapy.Field()
    url = scrapy.Field()
    source = scrapy.Field()


