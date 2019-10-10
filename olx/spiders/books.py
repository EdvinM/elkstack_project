# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from olx.items import BookItem


class BooksSpider(CrawlSpider):
    name = "books"
    allowed_domains = ["www.martinus.sk"]
    start_urls = ['https://www.martinus.sk/?uMod=list&uTyp=sklad&type=kniha&page=1']

    rules = (
        Rule(LinkExtractor(allow=(), restrict_css=('.btn--ghost',)),
             callback="parse_item",
             follow=False),)

    def parse_item(self, response):
        item_links = response.css('a.link--product::attr(href)').extract()
        for a in item_links:
            yield scrapy.Request(response.urljoin(a), callback=self.parse_detail_page)

    def parse_detail_page(self, response):

        # Check if language of parsed book is slovak, if not skip this book.
        language = self.parse_response_xpath(response,
                                             '//*[@id="details"]/div/div/div[1]/div/dl[dt="Jazyk"][1]/dd/text()')

        if language != "slovenský":
            pass

        title = self.parse_response_selector(response, 'h1.product-detail__title::text', 0)
        image_url = 'http:' + self.parse_response_selector(response, '.product-detail__image a.mj-product-preview img::attr(src)', 0)
        author = self.parse_response_selector(response, 'ul.product-detail__author a.link::text', 0)
        publisher = self.parse_response_selector(response, '.bar__item dl.no-mrg a.link::text', 0)
        description = self.html_to_text(self.parse_response_selector(response, 'section#description div.cms-article', 0))
        price = self.correct_price(self.parse_response_xpath(response,
                                                             '//*[@id="web"]/article/div[1]/div/div[1]/div/text()'))
        normal_price = self.correct_price(self.parse_response_xpath(response,
                                                                    '//*[@id="web"]/article/div[1]/div/div[2]/p/span[3]/text()'))
        discount = self.correct_discount(self.parse_response_xpath(response,
                                                                   '//*[@id="web"]/article/div[1]/div/div[2]/div[1]/div/text()'))

        # Book Details
        original_name = self.parse_response_xpath(response,
                                                  '//*[@id="details"]/div/div/div[1]/div/dl[dt="Originálny názov"][1]/dd/text()')
        page_number = self.parse_response_xpath(response,
                                                '//*[@id="details"]/div/div/div[1]/div/dl[dt="Počet strán"][1]/dd/text()')
        pledge = self.parse_response_xpath(response,
                                           '//*[@id="details"]/div/div/div[1]/div/dl[dt="Väzba"][1]/dd/text()')
        size = self.parse_response_xpath(response, '//*[@id="details"]/div/div/div[1]/div/dl[dt="Rozmer"][1]/dd/text()')
        weight = self.parse_response_xpath(response,
                                           '//*[@id="details"]/div/div/div[1]/div/dl[dt="Hmotnosť"][1]/dd/text()')
        isbn = self.parse_response_xpath(response, '//*[@id="details"]/div/div/div[1]/div/dl[dt="ISBN"][1]/dd/text()')
        release_year = self.parse_response_xpath(response,
                                                 '//*[@id="details"]/div/div/div[1]/div/dl[dt="Rok vydania"][1]/dd/text()')
        publishing_house = self.parse_response_xpath(response,
                                                     '//*[@id="details"]/div/div/div[1]/div/dl[dt="Vydavateľstvo"][1]/dd/text()')
        cat_number = self.parse_response_xpath(response,
                                               '//*[@id="details"]/div/div/div[1]/div/dl[dt="Naše katalógové číslo"][1]/dd/text()')

        item = BookItem()
        item['id'] = response.url.split('=')[1]
        item['title'] = title
        item['image_url'] = image_url
        item['author'] = author
        item['publisher'] = publisher
        item['description'] = description
        item['price'] = price
        item['normal_price'] = normal_price
        item['discount'] = discount
        item['original_name'] = original_name
        item['page_number'] = page_number
        item['pledge'] = pledge
        item['size'] = size
        item['weight'] = weight
        item['language'] = language
        item['isbn'] = isbn
        item['release_year'] = release_year
        item['publishing_house'] = publishing_house
        item['cat_number'] = cat_number
        item['url'] = response.url

        yield item

    def parse_response_xpath(self, response, selector):
        resp = response.xpath(selector).get()

        if resp is None:
            return resp

        return resp.strip()

    def parse_response_selector(self, response, selector, index):
        resp = response.css(selector).extract()

        if resp is None:
            return resp

        if len(resp) == 0:
            return resp

        return resp[index].strip()

    def html_to_text(self, text):
        """Remove html tags from a string"""
        import re
        # First, create a pattern to remove html tags
        clean = re.compile('<.*?>')

        # Remove HMTL tags & \r\n.
        text_ = re.sub(clean, '', text).strip().replace("\r\n", " ")

        # Add space after punctuation characters
        text_ = re.sub('([.!?)])', r'\1 ', text_)

        # Return clean text, without extra spaces gaine after punctuation space addition.
        return re.sub('\s{2,}', ' ', text_).replace(". . .", "...")

    def correct_price(self, price):
        if price is None:
            return price

        return price.strip().replace(u'\xa0', u' ')

    def correct_discount(self, discount):
        if discount is None:
            return discount

        split_ = discount.split(' ')

        if len(split_) == 1:
            return split_[0]

        return split_[1]
