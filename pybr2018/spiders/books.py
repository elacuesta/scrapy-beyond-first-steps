# -*- coding: utf-8 -*-
from collections import deque
from scrapy import Spider, signals


class BooksSpider(Spider):
    """
    Base spider with common methods to extract links and book data
    """
    name = 'books'
    start_urls = ['http://books.toscrape.com']

    custom_settings = {
        'SPIDER_MIDDLEWARES': {
            'pybr2018.middlewares.books.BookCacheSpiderMiddleware': 543,
        },
        'ITEM_PIPELINES': {
            'pybr2018.pipelines.ValidateBookPipeline': 100,
        },
    }

    def parse(self, response):
        for book_link in response.css('article.product_pod h3 a::attr(href)').getall():
            self.logger.info('Scheduling: %s', book_link)
            yield response.follow(book_link, callback=self.parse_book)

    def parse_book(self, response):
        self.logger.info('Extracting: %s', response.url)
        return {
            'url': response.url,
            'title': response.css('h1::text').get(),
            'price': float(response.css('p.price_color::text').re_first(r'(\d+.?\d*)')),
        }


class SequentialBooksSpider(BooksSpider):
    """
    A spider that schedules and processes requests/responses sequentially
    """
    name = 'books-sequential'

    custom_settings = {
        'SCHEDULER': 'pybr2018.scheduler.SequentialScheduler',
        'SCHEDULER_DISK_QUEUE': 'scrapy.squeues.PickleFifoDiskQueue',
        'SCHEDULER_MEMORY_QUEUE': 'scrapy.squeues.FifoMemoryQueue',
    }

    def parse(self, response):
        for book_link in response.css('article.product_pod h3 a::attr(href)'):
            self.logger.info('Yielding request: %s', book_link.get())
            yield response.follow(book_link, callback=self.parse_book)
            yield response.request.replace(dont_filter=True, callback=self.parse_dummy)

    def parse_dummy(self, response):
        self.logger.info('Back at the main page')
