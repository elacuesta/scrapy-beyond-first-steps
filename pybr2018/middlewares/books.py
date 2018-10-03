import os
import json
import logging

import scrapy


class BookCacheSpiderMiddleware:
    """
    Avoid making requests if we already have the item we need
    """
    @classmethod
    def from_crawler(cls, crawler):
        mw = cls()
        mw.crawler = crawler
        mw.logger = logging.getLogger(cls.__name__)
        with open('{}/../data/books.cache'.format(os.path.dirname(__file__)), 'r') as f:
            mw.books = {item['url']: item for item in json.load(f)}
        mw.logger.info('Found %i cached books', len(mw.books))
        return mw

    def process_spider_output(self, response, result, spider):
        for elem in result:
            if isinstance(elem, scrapy.Request) and elem.url in self.books:
                self.logger.info('[%s] Book found in cache, not making request', elem.url)
                self.crawler.stats.inc_value('book_from_cache')
                item = self.books[elem.url]
                item['_cache'] = True
                yield self.books[elem.url]
            else:
                yield elem
