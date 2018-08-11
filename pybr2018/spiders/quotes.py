import scrapy

from pybr2018.items import QuoteItemLoader


class QuotesSpider(scrapy.Spider):
    """
    A spider that extracts quotes from multiple versions of the same site (HTML, b64, zipped)
    """
    name = 'quotes'
    start_urls = [
        'http://localhost:8000/Quotes.html',          # raw HTML
        'http://localhost:8000/Quotes2.b64.txt',      # b64 encoded HTML
        'http://localhost:8000/Quotes3.b64.txt.zip',  # b64 encoded HTML, zipped
    ]
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
           'pybr2018.downloader_middlewares.quotes.DecompressZipMiddleware': 543,
           'pybr2018.downloader_middlewares.quotes.DecodeBase64Middleware': 542,
        },
        # 'ITEM_PIPELINES': {'pybr2018.pipelines.ValidateQuotesPipeline': 100},
    }

    def parse(self, response):
        for quote in response.css('div.quote'):
            loader = QuoteItemLoader(selector=quote)
            loader.add_value('url', response.url)
            loader.add_css('author', 'small.author::text')
            loader.add_css('text', 'span.text::text')
            loader.add_css('tags', 'meta.keywords::attr(content)')
            yield loader.load_item()
