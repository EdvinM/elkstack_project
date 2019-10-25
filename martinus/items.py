# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

# Poskrapeovat iba jazyk - slovensky

class BookItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    title = scrapy.Field()
    image_url = scrapy.Field()
    author = scrapy.Field()
    publisher = scrapy.Field()
    description = scrapy.Field()
    price = scrapy.Field()
    normal_price = scrapy.Field()
    discount = scrapy.Field()

    original_name = scrapy.Field()

    page_number = scrapy.Field()
    pledge = scrapy.Field()
    size = scrapy.Field()

    weight = scrapy.Field()
    language = scrapy.Field()
    isbn = scrapy.Field()

    release_year = scrapy.Field()
    publishing_house = scrapy.Field()
    cat_number = scrapy.Field()

    url = scrapy.Field()
