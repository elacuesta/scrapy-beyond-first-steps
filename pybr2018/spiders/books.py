# -*- coding: utf-8 -*-
import scrapy


class BaseBooksSpider(scrapy.Spider):
    """
    Common methods to navigate the site and extract book data
    """

    def start_requests(self):
        yield scrapy.Request('http://books.toscrape.com', callback=self.extract_book_urls)

    def extract_book_urls(self, response):
        return map(response.urljoin, response.css('article.product_pod h3 a::attr(href)').getall())

    def parse_book(self, response):
        self.logger.info('Extracting book from %s', response.url)
        return {
            'url': response.url,
            'title': response.css('h1::text').get(),
            'price': response.css('p.price_color::text').get(),
            'image_url': response.urljoin(response.css('div.thumbnail img::attr(src)').get()),
            'rating': response.css('p.star-rating::attr(class)').get('').split(' ')[-1],
        }


class ParallelBooksSpider(BaseBooksSpider):
    """
    A spider that schedules and processes requests/responses in parallel
    """
    name = 'books-parallel'

    def extract_book_urls(self, response):
        for book_url in super().extract_book_urls(response):
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

    def extract_book_urls(self, response):
        for link in super().extract_book_urls(response):
            self.pending_book_urls.add(link)
