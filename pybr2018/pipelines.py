import re
import logging

from scrapy.exceptions import DropItem
import jsonschema


class AveragePipeline:

    prices = []
    ratings = []

    def __init__(self, *args, **kwargs):
        self.logger = logging.getLogger(self.__class__.__name__)

    def process_item(self, item, spider):
        price = re.search(r'(\d+.?\d*)', item['price']).group(1)
        self.prices.append(float(price))
        self.ratings.append(item['rating'])
        return item

    def close_spider(self, spider):
        self.logger.info('Processed items: {}'.format(len(self.prices)))
        self.logger.info('Minimum price: {}'.format(min(self.prices)))
        self.logger.info('Maximum price: {}'.format(max(self.prices)))
        self.logger.info('Average price: {}'.format(sum(self.prices)/len(self.prices)))
        self.logger.info('Minimum rating: {}'.format(min(self.ratings)))
        self.logger.info('Maximum rating: {}'.format(max(self.ratings)))
        self.logger.info('Average rating: {}'.format(sum(self.ratings)/len(self.ratings)))


class ValidateQuotesPipeline:
    schema = {
        '$schema': 'http://json-schema.org/draft-07/schema#',
        '$id': 'http://example.com/product.schema.json',
        'title': 'Quote',
        'type': 'object',
        'properties': {
            'text': {
                'type': 'string',
                'maxLength': 120
            },
            'tags': {
                'type': 'array',
                'items': {
                    'type': 'string'
                },
                'minItems': 1,
                'maxItems': 3,
            }
        },
        'additionalProperties': True,
    }

    def process_item(self, item, spider):
        try:
            jsonschema.validate(item, self.schema)
        except jsonschema.ValidationError as ex:
            raise DropItem(ex.message)
        else:
            return item
