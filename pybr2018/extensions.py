import logging

from twisted.internet import defer, reactor
from scrapy import signals


class RemoteStorageExtension:
    """
    Write items to a remote storage server (Proof of concept, write to file instead).
    Optimize blocking operations by returning Twisted Deferreds
    (imagine the operations could take a long time)
    """

    @classmethod
    def from_crawler(cls, crawler):
        ext = cls()
        ext.logger = logging.getLogger(cls.__name__)
        crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(ext.item_scraped, signal=signals.item_scraped)
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
        return ext

    def spider_opened(self, spider):
        self.logger.info('Writing items to a remote location')
        self.file = open('{}_items.txt'.format(spider.name), 'w')

    def item_scraped(self, item, response, spider):
        dfd = defer.Deferred()
        dfd.addCallback(self._write_item)
        reactor.callLater(0, dfd.callback, item)
        return dfd

    def _write_item(self, item):
        row = ', '.join([
            '{}: {}'.format(key, value) for key, value in
            sorted(dict(item).items(), key=lambda elem: elem[0])
        ])
        self.file.write(row + '\n')
        return item

    def spider_closed(self, spider, reason):
        self.file.close()
