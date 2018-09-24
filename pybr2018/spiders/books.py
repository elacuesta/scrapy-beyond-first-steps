# -*- coding: utf-8 -*-
import scrapy


class BooksSpider(scrapy.Spider):
    """
    Base spider with common methods to extract links and book data
    """
    name = 'books'
    start_urls = ['http://books.toscrape.com']

    def extract_book_urls(self, response):
        return map(response.urljoin, response.css('article.product_pod h3 a::attr(href)').getall())

    def parse(self, response):
        for book_url in self.extract_book_urls(response):
            self.logger.info('Scheduling: %s', book_url)
            yield scrapy.Request(book_url, callback=self.parse_book)

    def parse_book(self, response):
        self.logger.info('Extracting: %s', response.url)
        return {
            'url': response.url,
            'title': response.css('h1::text').get(),
            'price': response.css('p.price_color::text').get(),
            'rating': response.css('p.star-rating::attr(class)').get('').split()[-1],
        }


class SequentialBooksSpider(BooksSpider):
    """
    A spider that schedules and processes requests/responses sequentially
    """
    name = 'books-sequential'
    pending = []

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super().from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.schedule_request, signal=scrapy.signals.spider_idle)
        return spider

    def schedule_request(self):
        if self.pending:
            request = self.pending.pop()
            self.logger.info('Scheduling: %s', request.url)
            self.crawler.engine.crawl(request, self)

    def parse(self, response):
        for book_url in self.extract_book_urls(response):
            self.pending.append(scrapy.Request(book_url, callback=self.parse_book))
            self.pending.append(response.request.replace(dont_filter=True, callback=self.parse_dummy))

    def parse_dummy(self, response):
        self.logger.info('Back at the main page')
