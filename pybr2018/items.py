from scrapy import Item, Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Identity, Compose


class QuoteItem(Item):
    url = Field()
    author = Field()
    text = Field()
    tags = Field()


class QuoteItemLoader(ItemLoader):
    default_item_class = QuoteItem
    default_input_processor = Identity()
    default_output_processor = TakeFirst()

    tags_out = Compose(TakeFirst(), lambda s: s.split(','))
