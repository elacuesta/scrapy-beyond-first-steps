# -*- coding: utf-8 -*-
import scrapy


numeric_ratings = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5}


class BooksSpider(scrapy.Spider):
    """
    Base spider with common methods to extract links and book data
    """
    name = 'books'
    start_urls = ['http://books.toscrape.com']
    custom_settings = {
        'ITEM_PIPELINES': {
            'pybr2018.pipelines.BlockingStoragePipeline': 110,
        },
    }

    def extract_book_urls(self, response):
        return map(response.urljoin, response.css('article.product_pod h3 a::attr(href)').getall())

    def parse(self, response):
        for book_url in self.extract_book_urls(response):
            self.logger.info('Scheduling request for %s', book_url)
            yield scrapy.Request(book_url, callback=self.parse_book)

    def parse_book(self, response):
        self.logger.info('Extracting book from %s', response.url)
        rating = response.css('p.star-rating::attr(class)').get('').split(' ')[-1]
        return {
            'url': response.url,
            'title': response.css('h1::text').get(),
            'price': response.css('p.price_color::text').get(),
            'rating': numeric_ratings.get(rating.lower()),
        }


class SequentialBooksSpider(BooksSpider):
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
