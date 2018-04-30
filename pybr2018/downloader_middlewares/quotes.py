# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

# From https://doc.scrapy.org/en/latest/topics/downloader-middleware.html:
# The process_request() method of each middleware will be invoked in increasing
# middleware order (100, 200, 300, …) and the process_response() method of each
# middleware will be invoked in decreasing order.

import logging
from io import BytesIO
from zipfile import ZipFile, BadZipfile
from base64 import b64decode

import scrapy


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class DecompressZipMiddleware(object):

    def process_response(self, request, response, spider):
        """
        Decompress a zipped response
        """
        try:
            z = ZipFile(BytesIO(response.body))
        except BadZipfile:
            logger.info('[%s] Not a zip file', response.url)
            return response
        else:
            logger.info('[%s] Decompressing response', response.url)
            name = z.namelist()[0]
            content = z.read(name)
            return scrapy.http.Response(url=response.url, body=content)


class DecodeBase64Middleware(object):

    def process_response(self, request, response, spider):
        """
        Decode a Base64-encoded response
        """
        decoded = b64decode(response.body)
        try:
            scrapy.selector.Selector(text=decoded.decode('utf8'))
        except UnicodeDecodeError:  # :see_no_evil:
            logger.info('[%s] Not a b64-encoded response', response.url)
            return response
        else:
            logger.info('[%s] Decoded base64 response', response.url)
            return scrapy.http.TextResponse(url=response.url, body=decoded)
