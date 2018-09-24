import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = [
        'http://quotes.toscrape.com/',
        'http://quotes.toscrape.com/page/2/',
        'http://quotes.toscrape.com/page/3/',
    ]
    custom_settings = {
        'ITEM_PIPELINES': {'pybr2018.pipelines.ValidateQuotesPipeline': 100},
    }

    def parse(self, response):
        for quote in response.css('div.quote'):
            item = {
                'url': response.url,
                'author': quote.css('small.author::text').get(),
                'text': quote.css('span.text::text').get(),
                'tags': quote.css('meta.keywords::attr(content)').get() or '',
            }
            item['tags'] = list(filter(None, item['tags'].split(',')))
            yield item
