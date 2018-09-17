from scrapy import Spider, Request


class DegreesSpider(Spider):
    """
    A spider that converts from Celsius to Fahrenheit and vice-versa using an external SOAP service
    """
    name = 'degrees'
    url = 'https://www.w3schools.com/xml/tempconvert.asmx'
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
           'pybr2018.middlewares.temperature.TemperatureConversionMiddleware': 543,
        }
    }

    def make_request(self, operation_name, source_value):
        return Request(
            url=self.url,
            dont_filter=True,
            meta={'source_value': source_value, 'operation_name': operation_name},
        )

    def start_requests(self):
        yield self.make_request('CelsiusToFahrenheit', 0)
        yield self.make_request('CelsiusToFahrenheit', 1)
        yield self.make_request('CelsiusToFahrenheit', 15.6)
        yield self.make_request('FahrenheitToCelsius', 100)
        yield self.make_request('FahrenheitToCelsius', 451)
        yield self.make_request('FahrenheitToCelsius', 10)

    def parse(self, response):
        source, destination = response.meta['operation_name'].split('To')
        return {
            'source_unit': source,
            'destination_unit': destination,
            'source_value': response.meta['source_value'],
            'destination_value': response.meta['result'],
        }
