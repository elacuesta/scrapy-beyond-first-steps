import random

import scrapy


class TemperatureSpider(scrapy.Spider):
    """
    A spider that converts from Celsius to Fahrenheit and vice-versa using an external SOAP service
    """
    name = 'temperature'
    url = 'https://www.w3schools.com/xml/tempconvert.asmx'
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
           'pybr2018.middlewares.temperature.TemperatureConversionMiddleware': 543,
        }
    }

    def start_requests(self):
        for operation in ('CelsiusToFahrenheit', 'FahrenheitToCelsius'):
            for _ in range(5):
                meta = {'operation_name': operation, 'source_value': random.uniform(0, 50)}
                yield scrapy.Request(self.url, dont_filter=True, meta=meta)

    def parse(self, response):
        # scrapy.shell.inspect_response(response, self)
        source_unit, destination_unit = response.meta['operation_name'].split('To')
        return {
            'source': '{} {}'.format(response.meta['source_value'], source_unit),
            'destination': '{} {}'.format(response.meta['result'], destination_unit),
        }
