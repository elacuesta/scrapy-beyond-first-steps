# -*- coding: utf-8 -*-
import scrapy


class BaseBooksSpider(scrapy.Spider):
    """
    Abstract spider with common methods to extract links and book data
    """
    start_urls = ['http://books.toscrape.com']

    def extract_book_urls(self, response):
        return map(response.urljoin, response.css('article.product_pod h3 a::attr(href)').getall())

    def parse_book(self, response):
        self.logger.info('Extracting book from %s', response.url)
        return {
            'url': response.url,
            'title': response.css('h1::text').get(),
            'price': response.css('p.price_color::text').get(),
            'rating': response.css('p.star-rating::attr(class)').get('').split(' ')[-1],
        }


class ParallelBooksSpider(BaseBooksSpider):
    """
    A spider that schedules and processes requests/responses in parallel
    """
    name = 'books-parallel'

    def parse(self, response):
        for book_url in self.extract_book_urls(response):
            self.logger.info('Scheduling request for %s', book_url)
            yield scrapy.Request(book_url, callback=self.parse_book)


class SequentialBooksSpider(BaseBooksSpider):
    """
    A spider that schedules and processes requests/responses sequentially
    """
    name = 'books-sequential'

    pending_book_urls = set()

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super().from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.schedule_request, signal=scrapy.signals.spider_idle)
        return spider

    def schedule_request(self):
        if self.pending_book_urls:
            book_url = self.pending_book_urls.pop()
            self.logger.info('Scheduling request for %s', book_url)
            request = scrapy.Request(book_url, callback=self.parse_book)
            self.crawler.engine.crawl(request, self)

    def parse(self, response):
        for link in self.extract_book_urls(response):
            self.pending_book_urls.add(link)
