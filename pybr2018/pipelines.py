import re
import logging

from twisted.internet import defer, reactor
from scrapy.exceptions import DropItem
import jsonschema


class BlockingStoragePipeline:
    """
    Optimize a blocking writing operation by returning a Twisted Deferred
    (imagine the operation could take a long time, like writing a remote database)
    """
    def open_spider(self, spider):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.file = open('{}_items.txt'.format(spider.name), 'w')

    def process_item(self, item, spider):
        dfd = defer.Deferred()
        dfd.addCallback(self.write_item)
        reactor.callLater(0, dfd.callback, item)
        return dfd

    def write_item(self, item):
        self.logger.info('Writing to a remote destination: %s', self.file.name)
        row = ', '.join([
            '{}: {}'.format(key, value) for key, value in
            sorted(dict(item).items(), key=lambda elem: elem[0])
        ])
        self.file.write(row + '\n')
        return item

    def close_spider(self, spider):
        self.file.close()


class ValidateQuotesPipeline:
    """
    Validate each item with JSON Schema
    """
    schema = {
        '$schema': 'http://json-schema.org/draft-07/schema#',
        '$id': 'http://example.com/product.schema.json',
        'title': 'Quote',
        'type': 'object',
        'properties': {
            'url': {
                'type': 'string',
            },
            'author': {
                'type': 'string',
            },
            'text': {
                'type': 'string',
                'maxLength': 200,
            },
            'tags': {
                'type': 'array',
                'items': {
                    'type': 'string',
                },
                'minItems': 2,
                'maxItems': 5,
            }
        },
        'additionalProperties': True,
        'required': ['url', 'author', 'text', 'tags'],
    }

    def process_item(self, item, spider):
        try:
            jsonschema.validate(dict(item), self.schema)
        except jsonschema.ValidationError as ex:
            raise DropItem(ex.message)
        else:
            return item
