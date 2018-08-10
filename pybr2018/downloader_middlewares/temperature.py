import logging

from zeep import Client as ZeepClient
from scrapy import signals, Request
from lxml import etree


class _FakeResponse:
    """
    zeep.wsdl.bindings.soap.SoapBinding.process_reply expects a requests.models.Response object
    """
    def __init__(self, status_code, content, headers):
        self.status_code = status_code
        self.content = content
        self.headers = {k: v[0].decode('utf8') for k, v in headers.items()}


class TemperatureConversionMiddleware:
    """
    Use zeep to Make request bodies and parse responses.
    Put the parsed result under response.meta['result']
    """
    @classmethod
    def from_crawler(cls, crawler):
        mw = cls()
        mw.logger = logging.getLogger(cls.__name__)
        crawler.signals.connect(mw.spider_opened, signal=signals.spider_opened)
        return mw

    def spider_opened(self, spider):
        """
        Create the zeep Client using the WSDL from the spider.
        """
        self.client = ZeepClient('{}?WSDL'.format(spider.url))
        self.operations = list(self.client.wsdl.bindings.values())[0]

    def process_request(self, request, spider):
        if request.meta.get('zeep_ignore'):
            return None  # process normally
        else:
            operation_name = request.meta['operation_name']
            operation = self.operations.get(operation_name)
            self.logger.info('Creating request for "%s" operation', operation_name)
            source_unit, _ = operation_name.split('To')
            payload = dict()
            payload[source_unit] = request.meta['source_value']
            body = self.client.create_message(self.client.service, operation_name, **payload)
            return Request(
                url=request.url,
                method='POST',
                headers={
                    'Content-Type': 'text/xml; charset=utf-8',
                    'SOAPAction': operation.soapaction,
                },
                body=etree.tostring(body),
                dont_filter=True,
                meta={'zeep_ignore': True, **request.meta},
            )

    def process_response(self, request, response, spider):
        operation_name = request.meta['operation_name']
        operation = self.operations.get(operation_name)
        self.logger.info('Processing response for "%s" operation', operation_name)
        _response = _FakeResponse(response.status, response.body, response.headers)
        request.meta['result'] = self.operations.process_reply(self.client, operation, _response)
        return response
