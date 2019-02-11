# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LiveStreamItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    snippet = scrapy.Field()
    status = scrapy.Field()
    contentDetails = scrapy.Field()
    statistics = scrapy.Field()
    last_update = scrapy.Field()
    pass
