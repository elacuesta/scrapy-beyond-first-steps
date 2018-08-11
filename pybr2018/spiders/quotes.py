import scrapy


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
            yield {
                'url': response.url,
                'author': quote.css('small.author::text').get(),
                'text': quote.css('span.text::text').get(),
                'tags': quote.css('meta.keywords::attr(content)').get().split(','),
            }
