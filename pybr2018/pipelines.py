import re
import logging


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
